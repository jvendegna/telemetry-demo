FROM python:3.9
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY ./telemetry_demo/app.py .
COPY ./favicon.ico ./static/favicon.ico
CMD ["flask", "run"]