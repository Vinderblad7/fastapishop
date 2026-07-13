from fastapi import FastAPI
from src.main_router import main_router
from sqladmin import Admin
from src.database import engine
from src.admin import CategoryAdmin, authentication_backend

app = FastAPI()

app.include_router(main_router)

@app.get("/")
async def root():
    return {"status": "Backend is running!"} 

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(CategoryAdmin)