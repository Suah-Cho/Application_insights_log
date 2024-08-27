from fastapi import FastAPI, Request, Response
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from opentelemetry.trace import (
    SpanKind,
    get_tracer_provider,
    set_tracer_provider,
)
from opentelemetry.propagate import extract
from logging import getLogger, INFO
import os

app = FastAPI()

configure_azure_monitor(
    connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
)

tracer = trace.get_tracer(__name__, 
                          tracer_provider=trace.get_tracer_provider()
)

logger = getLogger(__name__)
logger.setLevel(INFO)

@app.middleware("http")
async def add_trace_data(request: Request, call_next):
    # Trace Context 추출
    with tracer.start_as_current_span(
        "main-20240827",
        context=extract(request.headers),
        kind=SpanKind.SERVER
    ) as span:
        # 요청 처리 전 로그 기록
        # logger.info("INFO log - Before Request.")
        
        # 요청 처리
        response = await call_next(request)

        # 요청 처리 후 로그 및 커스텀 속성 추가
        span.set_attribute('http.url', str(request.url))
        span.set_attribute('http.method', str(request.method))
        span.set_attribute('http.status_code', response.status_code)

        # logger.info("INFO log - After Request.")

        return response

@app.get('/')
def root():
    return {"message": "Hello, World!"}



@app.get('/test')
def test(request: Request):
    logger.info("INFO log - Test!!!!!!!!!!!!")
    return {"message": "Hello, Test!"}