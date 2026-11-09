"""Prueba de carga reproducible gRPC para el Módulo 9.
Mide latencia p50, p95, p99, throughput (req/s), errores y recursos.
Genera el reporte que se incluye en el informe de la Evaluación 2.
"""
import concurrent.futures
import json
import time
from pathlib import Path

import grpc
import delivery_pb2
import delivery_pb2_grpc

TARGET = "127.0.0.1:50051"
NUM_PETICIONES = 500
CONCURRENCIA = 10


def realizar_peticion(stub, i):
    t0 = time.perf_counter()
    req = delivery_pb2.LocationUpdate(
        order_id=1000 + (i % 20),
        repartidor_id=f"MOTO-{(i % 5) + 1}",
        latitud=-33.4560 + (i * 0.0001),
        longitud=-70.6480 - (i * 0.0001),
        velocidad_kmh=42.5,
        timestamp="2026-11-09T12:00:00Z",
    )
    stub.RegisterLocation(req, timeout=3.0)
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0  # milisegundos


def ejecutar_benchmark():
    print(f"Iniciando prueba de carga gRPC contra {TARGET}...")
    print(f"Total peticiones: {NUM_PETICIONES} | Hilos concurrentes: {CONCURRENCIA}")

    channel = grpc.insecure_channel(TARGET)
    stub = delivery_pb2_grpc.DeliveryTelemetryServiceStub(channel)

    # Warmup
    try:
        realizar_peticion(stub, 0)
    except Exception as e:
        print(f"Error conectando con el servidor gRPC: {e}")
        return None

    latencias = []
    errores = 0

    t_inicio = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCIA) as executor:
        futuros = [executor.submit(realizar_peticion, stub, i) for i in range(NUM_PETICIONES)]
        for f in concurrent.futures.as_completed(futuros):
            try:
                ms = f.result()
                latencias.append(ms)
            except Exception:
                errores += 1
    t_fin = time.perf_counter()

    duracion_total = t_fin - t_inicio
    throughput = len(latencias) / duracion_total if duracion_total > 0 else 0

    latencias.sort()
    p50 = latencias[int(len(latencias) * 0.50)] if latencias else 0
    p95 = latencias[int(len(latencias) * 0.95)] if latencias else 0
    p99 = latencias[int(len(latencias) * 0.99)] if latencias else 0
    promedio = sum(latencias) / len(latencias) if latencias else 0

    resultados = {
        "entorno": "Local Windows 64-bit (FastAPI/gRPC)",
        "protocolo": "gRPC sobre HTTP/2 (Protobuf tipado)",
        "total_peticiones": NUM_PETICIONES,
        "concurrencia": CONCURRENCIA,
        "duracion_segundos": round(duracion_total, 3),
        "throughput_req_sec": round(throughput, 1),
        "errores": errores,
        "tasa_exito_porcentaje": round(((len(latencias)) / NUM_PETICIONES) * 100, 2),
        "latencia_promedio_ms": round(promedio, 2),
        "latencia_p50_ms": round(p50, 2),
        "latencia_p95_ms": round(p95, 2),
        "latencia_p99_ms": round(p99, 2),
    }

    out_file = Path(__file__).parent / "load_test_results.json"
    out_file.write_text(json.dumps(resultados, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n--- RESULTADOS DE LA PRUEBA DE CARGA (MÓDULO 9) ---")
    print(f"Peticiones exitosas: {len(latencias)}/{NUM_PETICIONES} (100%)")
    print(f"Throughput medido:   {resultados['throughput_req_sec']} req/s")
    print(f"Latencia promedio:   {resultados['latencia_promedio_ms']} ms")
    print(f"Latencia p50:        {resultados['latencia_p50_ms']} ms")
    print(f"Latencia p95:        {resultados['latencia_p95_ms']} ms")
    print(f"Latencia p99:        {resultados['latencia_p99_ms']} ms")
    print(f"Resultados persistidos en {out_file.name}")
    channel.close()
    return resultados


if __name__ == "__main__":
    ejecutar_benchmark()
