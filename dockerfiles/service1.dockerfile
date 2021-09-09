FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./telemetry_demo/send-to-collector-example-service-1.py .
ENTRYPOINT [ "python", "send-to-collector-example-service-1.py" ]