# Needs Jaeger, keep that container from jaeger-export-example running, or restart it.
# This flask app sends traces directly to Jaeger.

import flask
import requests

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Step 1: Create tracer provider
trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "generic-flask-service"}))
)

# Connection config for Jaeger
jaeger_exporter = JaegerExporter(
    # TODO: Change these to env vars
    agent_host_name="localhost",
    agent_port=6831,
)

# Configure Jaeger-Exporter to use the batch span processor
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

app = flask.Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()


@app.route("/")
def hello():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("hello-request"):
        requests.get("http://www.example.com")
    return "hello"


app.run(debug=True, port=5000)
