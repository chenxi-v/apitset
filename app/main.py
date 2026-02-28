import logging
import os
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from app.api import router

error_logs = []

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MemoryHandler(logging.Handler):
    def emit(self, record):
        try:
            msg = self.format(record)
            error_logs.append(msg)
            if len(error_logs) > 100:
                error_logs.pop(0)
        except:
            pass

memory_handler = MemoryHandler()
memory_handler.setLevel(logging.ERROR)
logging.getLogger().addHandler(memory_handler)

app = FastAPI(
    title="TVBox 爬虫后端服务",
    description="实现 TVBox type: 3 爬虫源功能的后端服务",
    version="1.0.0",
    default_response_class=JSONResponse
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"请求错误: {request.method} {request.url} - {str(e)}", exc_info=True)
        raise

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "TVBox 爬虫后端服务",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/logs")
async def get_logs(lines: int = 100):
    return {"logs": error_logs[-lines:] if len(error_logs) > lines else error_logs}
