from azure.monitor.opentelemetry import configure_azure_monitor
from django.conf import settings
from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor

def _configure_otlp_exporter():
    """Configures the batch GRPC OTLP Span exporter and sets it as the tracer provider globally"""
    exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317")
    tracer_provider = TracerProvider()
    span_processor = BatchSpanProcessor(exporter)
    tracer_provider.add_span_processor(span_processor)

    trace.set_tracer_provider(tracer_provider)

    reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint="http://otel-collector:4317")
    )
    provider = MeterProvider(metric_readers=[reader])
    metrics.set_meter_provider(provider)


def _instrument_local():
    """Instruments the app manually for local collector usage"""
    _configure_otlp_exporter()
    DjangoInstrumentor().instrument()
    RequestsInstrumentor().instrument()
    Psycopg2Instrumentor().instrument()

def _instrument_azure():
    configure_azure_monitor()
    

def instrument_app():
    """Instruments the various layers of the application then configure exporters"""
    if settings.USE_AZURE_MONITOR:
        _instrument_azure()
    else:
        _instrument_local()
    # Manually instrument system metrics - Azure does not do this by default
    SystemMetricsInstrumentor().instrument()