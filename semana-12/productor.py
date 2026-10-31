import argparse
import json
import xml.etree.ElementTree as ET
from decimal import Decimal, InvalidOperation

import stomp

DESTINO = "/queue/pedidos"
LARGO_FIJO = 36  # ID[6] + CLIENTE[20] + MONTO[10]


def construir_mensaje(formato: str, pedido: dict, texto: str) -> tuple[str, str]:
    """Devuelve (cuerpo, mime-type) segun el formato pedido."""
    if formato == "texto":
        return texto, "text/plain; charset=utf-8"

    if formato == "fijo":
        identificador = str(pedido["id"])
        cliente = str(pedido["cliente"])
        monto = Decimal(pedido["monto"])
        if not (identificador.isascii() and identificador.isdigit() and len(identificador) <= 6):
            raise ValueError("En formato fijo, --id debe tener hasta 6 digitos ASCII")
        if len(cliente) > 20 or not cliente.isascii():
            raise ValueError("En formato fijo, --cliente admite hasta 20 caracteres ASCII")
        monto_campo = f"{monto:010.2f}"
        if monto < 0 or len(monto_campo) != 10:
            raise ValueError("En formato fijo, --monto debe estar entre 0 y 9999999.99")
        return f"{identificador.zfill(6)}{cliente:<20}{monto_campo}", "text/plain; charset=utf-8"

    if formato == "json":
        return json.dumps(pedido, ensure_ascii=False), "application/json; charset=utf-8"

    if formato == "xml":
        raiz = ET.Element("pedido")
        for clave, valor in pedido.items():
            ET.SubElement(raiz, clave).text = str(valor)
        return ET.tostring(raiz, encoding="unicode"), "application/xml; charset=utf-8"

    raise ValueError(f"Formato desconocido: {formato}")


def main():
    parser = argparse.ArgumentParser(description="Productor STOMP")
    parser.add_argument("--formato", choices=["texto", "fijo", "xml", "json"], required=True)
    parser.add_argument("--mensaje", default="Hola desde el productor STOMP")
    parser.add_argument("--id", default="123")
    parser.add_argument("--cliente", default="Ed Jobs")
    parser.add_argument("--monto", default="123.45")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=61613)
    parser.add_argument("--usuario", default="admin")
    parser.add_argument("--clave", default="admin")
    args = parser.parse_args()

    try:
        monto = Decimal(args.monto)
        if not monto.is_finite():
            raise ValueError("El monto debe ser un numero finito")
    except (InvalidOperation, ValueError):
        parser.error(f"Monto no valido: {args.monto}")

    pedido = {"id": args.id, "cliente": args.cliente, "monto": str(monto)}
    try:
        cuerpo, mime = construir_mensaje(args.formato, pedido, args.mensaje)
    except ValueError as exc:
        parser.error(str(exc))

    conexion = stomp.Connection12([(args.host, args.port)], vhost="localhost")
    try:
        conexion.connect(args.usuario, args.clave, wait=True)
        conexion.send(
            destination=DESTINO,
            body=cuerpo,
            headers={
                "content-type": mime,
                "x-formato": args.formato,
                "persistent": "true",
            },
        )
        print(f"Mensaje enviado a {DESTINO} (formato={args.formato}):\n{cuerpo}")
    finally:
        if conexion.is_connected():
            conexion.disconnect()


if __name__ == "__main__":
    main()
