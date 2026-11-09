"""Servidor gRPC para telemetría de reparto y analítica de cocina (:50051).
Módulo 9 - Implementación tipada con contratos Protobuf y streaming de eventos.
"""
import asyncio
import time
from concurrent import futures
import datetime

import grpc
import delivery_pb2
import delivery_pb2_grpc

PORT = "50051"

# Memoria de telemetría y métricas operacionales
_UBICACIONES = []
_METRICAS = {
    "total_pedidos": 42,
    "tiempo_promedio_cocina": 18.5,
    "throughput_hora": 28.0,
    "latencia_p95": 3.4,
    "despachos_en_ruta": 6,
}


class DeliveryTelemetryServicer(delivery_pb2_grpc.DeliveryTelemetryServiceServicer):
    def RegisterLocation(self, request, context):
        """Recepción de alta frecuencia y baja latencia de coordenadas de repartidores."""
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
        for etapa, lat, lng, mins in etapas:
            if context.is_active():
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


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    delivery_pb2_grpc.add_DeliveryTelemetryServiceServicer_to_server(DeliveryTelemetryServicer(), server)
    server.add_insecure_port(f"0.0.0.0:{PORT}")
    server.start()
    print(f"Servidor gRPC Delivery & Telemetry escuchando en puerto {PORT}...")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
