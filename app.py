from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.main import app as backend_app

main_app = FastAPI()

# Backend API at /api
main_app.mount("/api", backend_app)
# Frontend served at /
main_app.mount("/", StaticFiles(directory="static", html=True), name="static")

app = main_app  # Hugging Face expects this variable
