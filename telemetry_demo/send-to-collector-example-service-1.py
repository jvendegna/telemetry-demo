# Here we start getting more complex.
# To run this you will need to start the docker-compose stack.
# Depends on: Jaeger and the Collector running on the same network, and referencing each at the correct endpoint and port.
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# connection string for span exporter = the collector
span_exporter = OTLPSpanExporter(
    # optional
    endpoint := "otelcollector:4317",
    # credentials=ChannelCredentials(credentials),
    # headers=(("metadata", "metadata")),
)

# Set up a trace provider
tracer_provider = TracerProvider(
    resource=Resource.create({SERVICE_NAME: "send-to-collector-1"})
)
trace.set_tracer_provider(tracer_provider)
span_processor = BatchSpanProcessor(span_exporter)
tracer_provider.add_span_processor(span_processor)

# Configure the tracer to use the collector exporter
tracer = trace.get_tracer_provider().get_tracer(__name__)

with tracer.start_as_current_span("foo"):
    print("Hello from app1!")
