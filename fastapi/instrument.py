import os

import fastapi
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def _instrument_local(app: fastapi.FastAPI):
    """Instruments the app manually for local collector usage"""
    exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317")

    tracer_provider = TracerProvider()
    span_processor = BatchSpanProcessor(exporter)
    tracer_provider.add_span_processor(span_processor)

    trace.set_tracer_provider(tracer_provider)

    FastAPIInstrumentor.instrument_app(app)
    RequestsInstrumentor().instrument()

def _instrument_azure():
    configure_azure_monitor()
    

def instrument_app(app: fastapi.FastAPI):
    use_azure = os.environ.get("USE_AZURE_MONITOR")

    if use_azure and use_azure.lower() == "true":
        _instrument_azure()
    else:
        _instrument_local(app)