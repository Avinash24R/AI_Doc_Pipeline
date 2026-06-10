from fastapi import FastAPI
import time
from app.api.routes.upload import router

from app.db.database import engine
from app.db.models import Base
from app.db import models
from app.metrics_middleware import (
    MetricsMiddleware,
    metrics_router
)


for i in range(10):
    try:
        Base.metadata.create_all(bind=engine)
        print("Database connected")
        break
    except Exception as e:
        print("Waiting for database...")
        time.sleep(3)


app = FastAPI()

app.add_middleware(
    MetricsMiddleware
)

app.include_router(router)
app.include_router(
    metrics_router
)