from fastapi import FastAPI
from src.adapters.controllers.templates_http import router as templates_router

app = FastAPI(
    title="Invoice API",
    description="Invoice API",
    version="1.0.0"
)
app.include_router(templates_router)