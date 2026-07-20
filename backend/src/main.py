import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware # <-- 1. ИМПОРТИРУЕМ МИДЛВАРЬ
from src.main_router import main_router
from sqladmin import Admin
from src.database import engine
from src.admin import CategoryAdmin, ProductAdmin, authentication_backend

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],
)
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
STATIC_DIR = os.path.join(CURRENT_DIR, "static")

os.makedirs(os.path.join(STATIC_DIR, "uploads"), exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(main_router)

@app.get("/")
async def root():
    return {"status": "Backend is running!"} 

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(CategoryAdmin)
admin.add_view(ProductAdmin)