import os

from azure.monitor.opentelemetry import configure_azure_monitor
from flask import Flask
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def _instrument_local(app: Flask):
    exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317")

    tracer_provider = TracerProvider()
    span_processor = BatchSpanProcessor(exporter)
    tracer_provider.add_span_processor(span_processor)

    trace.set_tracer_provider(tracer_provider)

    FlaskInstrumentor().instrument_app(app)
    RequestsInstrumentor().instrument()

def _instrument_azure(app: Flask):
    configure_azure_monitor()
    # Manually instrument Flask afterwards?
    # FlaskInstrumentor().instrument_app(app)  

def instrument_app(app: Flask):
    use_azure = os.environ.get("USE_AZURE_MONITOR")

    if use_azure and use_azure.lower() == "true":
        _instrument_azure(app)
    else:
        _instrument_local(app)

def create_app():
    app = Flask(__name__)

    instrument_app(app)

    from .views import index_bp
    app.register_blueprint(index_bp)

    return app
