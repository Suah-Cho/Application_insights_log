from fastapi import FastAPI
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
import logging
import os

app = FastAPI()

connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")


resource = Resource.create({"service.name": "croft-test"})

provider = TracerProvider(resource=resource)
span_processor = BatchSpanProcessor(
    AzureMonitorTraceExporter.from_connection_string(connection_string)
)
provider.add_span_processor(span_processor)

from opentelemetry import trace
trace.set_tracer_provider(provider)

FastAPIInstrumentor.instrument_app(app)

@app.get('/')
def root():
    logging.info("test1 - info")
    logging.warning("test2 - warning")
    logging.error("test3 - error")
    return {"message": "Hello World"}

@app.get('/application')
def application():
    return {"message": "Hello World from application"}

@app.get('/insights')
def insights():
    return {"message": "Hello World from insights"}