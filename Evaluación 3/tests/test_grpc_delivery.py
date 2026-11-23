"""Pruebas de Integración y Streaming gRPC (Módulo 9).
Valida contratos .proto, servidor gRPC, streaming de eventos y analítica de cocina.
"""
import os
import grpc
import pytest

import delivery_pb2
import delivery_pb2_grpc
from grpc_server import crear_servidor


SECRETO = os.environ["GRPC_SERVICE_SECRET"]
AUTH = (("x-service-secret", SECRETO),)


@pytest.fixture(scope="module")
def servidor():
    server, port = crear_servidor(SECRETO, "127.0.0.1:0")
    server.start()
    yield port
    server.stop(0)


@pytest.fixture(scope="module")
def grpc_service(servidor):
    channel = grpc.insecure_channel(f"127.0.0.1:{servidor}")
    stub = delivery_pb2_grpc.DeliveryTelemetryServiceStub(channel)
    yield stub
    channel.close()


def test_grpc_rechaza_llamadas_sin_identidad_de_servicio(servidor):
    channel = grpc.insecure_channel(f"127.0.0.1:{servidor}")
    stub = delivery_pb2_grpc.DeliveryTelemetryServiceStub(channel)
    req = delivery_pb2.KitchenMetricsRequest(ventana_minutos=60)
    with pytest.raises(grpc.RpcError) as sin:
        stub.GetKitchenMetrics(req, timeout=3.0)
    assert sin.value.code() == grpc.StatusCode.UNAUTHENTICATED
    with pytest.raises(grpc.RpcError) as mala:
        stub.GetKitchenMetrics(req, timeout=3.0, metadata=(("x-service-secret", "incorrecto"),))
    assert mala.value.code() == grpc.StatusCode.UNAUTHENTICATED
    with pytest.raises(grpc.RpcError) as stream:
        list(stub.StreamOrderTracking(delivery_pb2.TrackingRequest(order_id=1), timeout=3.0))
    assert stream.value.code() == grpc.StatusCode.UNAUTHENTICATED
    channel.close()


def test_grpc_valida_entradas_y_deadline(grpc_service):
    malo = delivery_pb2.LocationUpdate(order_id=-5, repartidor_id="M", latitud=999, longitud=0, velocidad_kmh=1)
    with pytest.raises(grpc.RpcError) as e:
        grpc_service.RegisterLocation(malo, timeout=3.0, metadata=AUTH)
    assert e.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    # Deadline corto: el stream termina con DEADLINE_EXCEEDED en vez de colgar al cliente
    with pytest.raises(grpc.RpcError) as d:
        list(grpc_service.StreamOrderTracking(delivery_pb2.TrackingRequest(order_id=7), timeout=0.2, metadata=AUTH))
    assert d.value.code() == grpc.StatusCode.DEADLINE_EXCEEDED


def test_grpc_memoria_acotada():
    import grpc_server
    assert grpc_server._UBICACIONES.maxlen == grpc_server.MAX_UBICACIONES


def test_grpc_unary_register_location(grpc_service):
    req = delivery_pb2.LocationUpdate(
        order_id=1042,
        repartidor_id="MOTO-01",
        latitud=-33.4569,
        longitud=-70.6483,
        velocidad_kmh=38.0,
        timestamp="2026-11-09T12:30:00Z",
    )
    res = grpc_service.RegisterLocation(req, timeout=3.0, metadata=AUTH)
    assert res.recibido is True
    assert "1042" in res.mensaje
    assert res.tiempo_servidor != ""


def test_grpc_server_streaming_tracking(grpc_service):
    req = delivery_pb2.TrackingRequest(order_id=1042, client_token="token-test")
    stream = grpc_service.StreamOrderTracking(req, timeout=5.0, metadata=AUTH)
    eventos = list(stream)

    assert len(eventos) == 4
    etapas = [e.etapa for e in eventos]
    assert etapas == ["en_preparacion", "en_camino", "llegando", "entregado"]
    assert eventos[-1].minutos_estimados == 0


def test_grpc_kitchen_analytics_metrics(grpc_service):
    req = delivery_pb2.KitchenMetricsRequest(ventana_minutos=30)
    res = grpc_service.GetKitchenMetrics(req, timeout=3.0, metadata=AUTH)
    assert res.total_pedidos_activos > 0
    assert res.throughput_pedidos_hora > 0
    assert res.latencia_p95_ms > 0
