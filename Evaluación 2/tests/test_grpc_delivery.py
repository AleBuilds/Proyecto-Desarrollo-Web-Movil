"""Pruebas de Integración y Streaming gRPC (Módulo 9).
Valida contratos .proto, servidor gRPC, streaming de eventos y analítica de cocina.
"""
from concurrent import futures
import grpc
import pytest

import delivery_pb2
import delivery_pb2_grpc
from grpc_server import DeliveryTelemetryServicer


@pytest.fixture(scope="module")
def grpc_service():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    delivery_pb2_grpc.add_DeliveryTelemetryServiceServicer_to_server(DeliveryTelemetryServicer(), server)
    port = server.add_insecure_port("127.0.0.1:0")
    server.start()
    channel = grpc.insecure_channel(f"127.0.0.1:{port}")
    stub = delivery_pb2_grpc.DeliveryTelemetryServiceStub(channel)
    yield stub
    server.stop(0)
    channel.close()


def test_grpc_unary_register_location(grpc_service):
    req = delivery_pb2.LocationUpdate(
        order_id=1042,
        repartidor_id="MOTO-01",
        latitud=-33.4569,
        longitud=-70.6483,
        velocidad_kmh=38.0,
        timestamp="2026-11-09T12:30:00Z",
    )
    res = grpc_service.RegisterLocation(req, timeout=3.0)
    assert res.recibido is True
    assert "1042" in res.mensaje
    assert res.tiempo_servidor != ""


def test_grpc_server_streaming_tracking(grpc_service):
    req = delivery_pb2.TrackingRequest(order_id=1042, client_token="token-test")
    stream = grpc_service.StreamOrderTracking(req, timeout=5.0)
    eventos = list(stream)

    assert len(eventos) == 4
    etapas = [e.etapa for e in eventos]
    assert etapas == ["en_preparacion", "en_camino", "llegando", "entregado"]
    assert eventos[-1].minutos_estimados == 0


def test_grpc_kitchen_analytics_metrics(grpc_service):
    req = delivery_pb2.KitchenMetricsRequest(ventana_minutos=30)
    res = grpc_service.GetKitchenMetrics(req, timeout=3.0)
    assert res.total_pedidos_activos > 0
    assert res.throughput_pedidos_hora > 0
    assert res.latencia_p95_ms > 0
