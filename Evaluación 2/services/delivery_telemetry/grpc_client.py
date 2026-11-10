"""Cliente gRPC reutilizable para integración interna."""
import os
import grpc
try:
    from . import delivery_pb2, delivery_pb2_grpc
except ImportError:
    import delivery_pb2, delivery_pb2_grpc

SERVER_ADDR = "127.0.0.1:50051"


class DeliveryClient:
    def __init__(self, target: str = SERVER_ADDR, secreto: str | None = None):
        self._metadata = (("x-service-secret", secreto or os.environ["GRPC_SERVICE_SECRET"]),)
        self.channel = grpc.insecure_channel(target)
        self.stub = delivery_pb2_grpc.DeliveryTelemetryServiceStub(self.channel)

    def registrar_posicion(self, order_id: int, repartidor_id: str, lat: float, lng: float, velocidad: float = 35.0):
        req = delivery_pb2.LocationUpdate(
            order_id=order_id,
            repartidor_id=repartidor_id,
            latitud=lat,
            longitud=lng,
            velocidad_kmh=velocidad,
            timestamp="2026-11-09T12:00:00Z",
        )
        return self.stub.RegisterLocation(req, timeout=2.0, metadata=self._metadata)

    def seguir_pedido_stream(self, order_id: int):
        req = delivery_pb2.TrackingRequest(order_id=order_id, client_token="token-demo")
        for event in self.stub.StreamOrderTracking(req, timeout=10.0, metadata=self._metadata):
            yield {
                "order_id": event.order_id,
                "etapa": event.etapa,
                "lat": event.latitud,
                "lng": event.longitud,
                "minutos_estimados": event.minutos_estimados,
                "secuencia": event.secuencia,
            }

    def obtener_metricas(self, ventana_minutos: int = 60):
        req = delivery_pb2.KitchenMetricsRequest(ventana_minutos=ventana_minutos)
        res = self.stub.GetKitchenMetrics(req, timeout=2.0, metadata=self._metadata)
        return {
            "pedidos_activos": res.total_pedidos_activos,
            "tiempo_cocina_min": res.tiempo_promedio_cocina_min,
            "throughput_hora": res.throughput_pedidos_hora,
            "latencia_p95_ms": res.latencia_p95_ms,
            "despachos_en_ruta": res.despachos_en_ruta,
        }

    def close(self):
        self.channel.close()
