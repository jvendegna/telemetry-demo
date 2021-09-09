FROM service1:local

COPY ./telemetry_demo/send-to-collector-example-service-2.py .
ENTRYPOINT [ "python", "send-to-collector-example-service-2.py" ]