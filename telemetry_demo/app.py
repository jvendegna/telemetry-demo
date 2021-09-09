# Flask app to send traces to the OTEL Collector, then forward them to Jaeger from there.
# Run in docker-compose

import flask
import requests
import os
from flask import send_from_directory

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

span_exporter = OTLPSpanExporter(
    # optional
    endpoint := "otelcollector:4317",
    # credentials=ChannelCredentials(credentials),
    # headers=(("metadata", "metadata")),
)
tracer_provider = TracerProvider(resource=Resource.create({SERVICE_NAME: "flask-app"}))
trace.set_tracer_provider(tracer_provider)
span_processor = BatchSpanProcessor(span_exporter)
tracer_provider.add_span_processor(span_processor)

# Configure the tracer to use the collector exporter
tracer = trace.get_tracer_provider().get_tracer(__name__)

app = flask.Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()


@app.route("/")
def hello():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("hello-request"):
        requests.get("http://www.example.com")
    return "hello"


@app.route("/add/<num1>/<num2>")
def add_two_numbers(num1, num2):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("add-two-numbers"):
        result = int(num1) + int(num2)
    return f"{num1} + {num2} = {str(result)}"


# Favicon will generate a 404 if not present.
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


app.run(debug=True, port=5000)
