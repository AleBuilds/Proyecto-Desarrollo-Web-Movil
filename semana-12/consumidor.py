import argparse
import json
import time
import xml.etree.ElementTree as ET

import stomp

DESTINO = "/queue/pedidos"
LARGO_FIJO = 36  


def interpretar(cuerpo: str, headers: dict):
    formato = headers.get("x-formato", "").lower()
    tipo_mime = headers.get("content-type", "").lower()
    if not formato:
        if "application/json" in tipo_mime:
            formato = "json"
        elif "application/xml" in tipo_mime or "text/xml" in tipo_mime:
            formato = "xml"
        else:
            formato = "texto"

    if formato == "texto":
        return formato, cuerpo

    if formato == "fijo":
        if len(cuerpo) != LARGO_FIJO:
            raise ValueError(f"Registro de ancho fijo invalido: {len(cuerpo)}, se esperan {LARGO_FIJO}")
        identificador = cuerpo[0:6]
        cliente = cuerpo[6:26].rstrip()
        monto = cuerpo[26:36]
        if not (
            identificador.isascii() and identificador.isdigit()
            and monto[:7].isdigit() and monto[7] == "." and monto[8:].isdigit()
        ):
            raise ValueError("Campos numericos de ancho fijo invalidos")
        return formato, {"id": identificador, "cliente": cliente, "monto": monto}

    if formato == "json":
        try:
            return formato, json.loads(cuerpo)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON invalido: {exc}") from exc

    if formato == "xml":
        try:
            raiz = ET.fromstring(cuerpo)
        except ET.ParseError as exc:
            raise ValueError(f"XML invalido: {exc}") from exc
        if raiz.tag != "pedido":
            raise ValueError("El nodo raiz de XML debe ser <pedido>")
        return formato, {elemento.tag: elemento.text for elemento in raiz}

    raise ValueError(f"Formato no soportado: {formato}")


class Escuchador(stomp.ConnectionListener):
    def __init__(self, conexion):
        self.conexion = conexion

    def on_error(self, frame):
        print(f"ERROR del broker: {frame.body}")

    def on_disconnected(self):
        print("Conexion STOMP cerrada")

    def on_message(self, frame):
        ack_id = frame.headers["ack"]
        try:
            formato, contenido = interpretar(frame.body, frame.headers)
            print(f"\n[RECIBIDO] formato={formato}")
            if isinstance(contenido, str):
                print(contenido)
            else:
                print(json.dumps(contenido, ensure_ascii=False, indent=2))
            self.conexion.ack(id=ack_id)
        except Exception as exc:
            print(f"[MENSAJE NO VALIDO] {exc}")
            self.conexion.nack(id=ack_id)


def main():
    parser = argparse.ArgumentParser(description="Consumidor STOMP")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=61613)
    parser.add_argument("--usuario", default="admin")
    parser.add_argument("--clave", default="admin")
    args = parser.parse_args()

    conexion = stomp.Connection12([(args.host, args.port)], vhost="localhost")
    conexion.set_listener("pedidos", Escuchador(conexion))
    try:
        conexion.connect(args.usuario, args.clave, wait=True)
        conexion.subscribe(
            destination=DESTINO, id="lector-pedidos",
            ack="client-individual", headers={"activemq.prefetchSize": "1"},
        )
        print(f"Escuchando {DESTINO}. Presiona Ctrl+C para salir.")
        while conexion.is_connected():
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nDeteniendo consumidor...")
    finally:
        if conexion.is_connected():
            conexion.disconnect()


if __name__ == "__main__":
    main()
