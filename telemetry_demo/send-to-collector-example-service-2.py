# Same as send-to-collector-example-service-1.py, with a different SERVICE_NAME
import uuid
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Define the exporter
span_exporter = OTLPSpanExporter(
    # optional
    endpoint := "otelcollector:4317",
    # credentials=ChannelCredentials(credentials),
    # headers=(("metadata", "metadata")),
)

# Set up a trace provider
tracer_provider = TracerProvider(
    resource=Resource.create({SERVICE_NAME: "send-to-collector-2"})
)
trace.set_tracer_provider(tracer_provider)
span_processor = BatchSpanProcessor(span_exporter)
tracer_provider.add_span_processor(span_processor)

# Configure the tracer to use the collector exporter
tracer = trace.get_tracer_provider().get_tracer(__name__)


with tracer.start_as_current_span("foo"):
    with tracer.start_as_current_span("bar"):
        # What not to do! Compare two traces from this service in Jaeger. I just wanted to see a divergence.
        id = uuid.uuid4()
        with tracer.start_as_current_span(str(id)):
            print("Hello from app2!")
