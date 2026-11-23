"""Servidor gRPC para telemetría de reparto y analítica de cocina (:50051).
Módulo 9 - Implementación tipada con contratos Protobuf y streaming de eventos.
"""
import hmac
import os
import time
from collections import deque
from concurrent import futures
import datetime

import grpc
import delivery_pb2
import delivery_pb2_grpc

PORT = os.getenv("GRPC_PORT", "50051")
# Solo escucha en loopback por defecto; en contenedores se define GRPC_BIND=0.0.0.0 dentro de la red privada.
BIND = os.getenv("GRPC_BIND", "127.0.0.1")
MAX_UBICACIONES = 10_000  # memoria acotada: descarta las mas antiguas

# Memoria de telemetría y métricas operacionales
_UBICACIONES = deque(maxlen=MAX_UBICACIONES)
_METRICAS = {
    "total_pedidos": 42,
    "tiempo_promedio_cocina": 18.5,
    "throughput_hora": 28.0,
    "latencia_p95": 3.4,
    "despachos_en_ruta": 6,
}


class AuthInterceptor(grpc.ServerInterceptor):
    """Autenticación de servicio: exige el secreto compartido en la metadata `x-service-secret`."""

    def __init__(self, secreto: str):
        self._secreto = secreto.encode("utf-8")

        def rechazar(_request, context):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Identidad de servicio no válida")

        self._rechazo = grpc.unary_unary_rpc_method_handler(rechazar)

    def intercept_service(self, continuation, handler_call_details):
        metadata = dict(handler_call_details.invocation_metadata or ())
        recibido = str(metadata.get("x-service-secret", "")).encode("utf-8")
        if hmac.compare_digest(recibido, self._secreto):
            return continuation(handler_call_details)
        return self._rechazo


class DeliveryTelemetryServicer(delivery_pb2_grpc.DeliveryTelemetryServiceServicer):
    def RegisterLocation(self, request, context):
        """Recepción de alta frecuencia y baja latencia de coordenadas de repartidores."""
        if request.order_id <= 0 or not (-90 <= request.latitud <= 90) or not (-180 <= request.longitud <= 180):
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Pedido o coordenadas fuera de rango")
        _UBICACIONES.append({
            "order_id": request.order_id,
            "repartidor": request.repartidor_id,
            "lat": request.latitud,
            "lng": request.longitud,
            "velocidad": request.velocidad_kmh,
            "ts": request.timestamp,
        })
        ahora = datetime.datetime.now().isoformat()
        return delivery_pb2.LocationResponse(
            recibido=True,
            mensaje=f"Coordenadas registradas para pedido #{request.order_id}",
            tiempo_servidor=ahora,
        )

    def StreamOrderTracking(self, request, context):
        """Server Streaming: emite progresivamente el avance geográfico y de estado del pedido."""
        etapas = [
            ("en_preparacion", -33.4560, -70.6480, 25),
            ("en_camino", -33.4585, -70.6520, 15),
            ("llegando", -33.4610, -70.6550, 5),
            ("entregado", -33.4625, -70.6570, 0),
        ]
        secuencia = 1
        if request.order_id <= 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Pedido inválido")
        for etapa, lat, lng, mins in etapas:
            restante = context.time_remaining()
            if context.is_active() and (restante is None or restante > 0):
                ahora = datetime.datetime.now().isoformat()
                yield delivery_pb2.TrackingEvent(
                    order_id=request.order_id,
                    etapa=etapa,
                    latitud=lat,
                    longitud=lng,
                    minutos_estimados=mins,
                    secuencia=secuencia,
                    timestamp=ahora,
                )
                secuencia += 1
                time.sleep(0.3)  # Intervalo de emisión controlado
            else:
                break

    def GetKitchenMetrics(self, request, context):
        """Analítica operacional de cocina y despacho."""
        return delivery_pb2.KitchenMetricsResponse(
            total_pedidos_activos=_METRICAS["total_pedidos"],
            tiempo_promedio_cocina_min=_METRICAS["tiempo_promedio_cocina"],
            throughput_pedidos_hora=_METRICAS["throughput_hora"],
            latencia_p95_ms=_METRICAS["latencia_p95"],
            despachos_en_ruta=_METRICAS["despachos_en_ruta"],
        )


def crear_servidor(secreto: str, direccion: str | None = None) -> tuple[grpc.Server, int]:
    """Servidor con autenticación de servicio, pool acotado y límite de tamaño de mensajes."""
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[AuthInterceptor(secreto)],
        maximum_concurrent_rpcs=100,
        options=[("grpc.max_receive_message_length", 64 * 1024)],
    )
    delivery_pb2_grpc.add_DeliveryTelemetryServiceServicer_to_server(DeliveryTelemetryServicer(), server)
    puerto = server.add_insecure_port(direccion or f"{BIND}:{PORT}")
    return server, puerto


def serve():
    server, _ = crear_servidor(os.environ["GRPC_SERVICE_SECRET"])
    server.start()
    print(f"Servidor gRPC Delivery & Telemetry escuchando en {BIND}:{PORT}...")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
