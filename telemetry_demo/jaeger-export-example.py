# Export a trace to Jaeger for better visualization of trace data.
# Needs Jaeger, so run it in Docker
# Docker Command to run Jaeger:
# `docker run -p 16686:16686 -p 6831:6831/udp jaegertracing/all-in-one`

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Step 1: Create tracer provider
trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "generic-hello-service"}))
)

# Connection config for Jaeger
jaeger_exporter = JaegerExporter(
    # TODO: Change these to env vars
    agent_host_name="localhost",
    agent_port=6831,
)

# Configure Jaeger-Exporter to use the batch span processor
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

# Set up the tracer
tracer = trace.get_tracer(__name__)

# Get to tracing
with tracer.start_as_current_span("foo"):
    with tracer.start_as_current_span("bar"):
        with tracer.start_as_current_span("baz"):
            print("Hello, World! - From OpenTelemetry Jaeger Example")
