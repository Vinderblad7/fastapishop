import os
import uuid
from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from sqlalchemy import select
from wtforms import FileField

from src.database import new_session
from src.users.models import UserModel
from src.categories.models import CategoryModel
from src.products.models import ProductModel
from src.users.utils import verify_password
from src.config import settings

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
UPLOAD_DIR = os.path.join(CURRENT_DIR, "static", "uploads")

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if not username or not password:
            return False

        async with new_session() as session:
            query = await session.execute(
                select(UserModel).where(UserModel.username == username)
            )
            user = query.scalar_one_or_none()
            
            if (
                user 
                and user.is_superuser
                and verify_password(password, user.hashed_password)
            ):
                request.session.update({"token": f"admin_token_{user.id}"})
                return True
                
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> RedirectResponse | bool:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"))

        return True

authentication_backend = AdminAuth(secret_key=settings.ADMIN_SECRET_KEY)

class CategoryAdmin(ModelView, model=CategoryModel):
    column_list = [CategoryModel.id, CategoryModel.name, CategoryModel.slug]
    name = "Category"
    name_plural = "Categories"
    icon = "fa-solid fa-list"


class ProductAdmin(ModelView, model=ProductModel):
    column_list = [ProductModel.id, ProductModel.name, ProductModel.price, ProductModel.category_id]
    form_columns = ["name", "description", "price", "category", "image_url"]
    
    form_overrides = {"image_url": FileField}
    
    name = "Product"
    name_plural = "Products"
    icon = "fa-solid fa-cart-shopping"

    async def on_model_change(self, data: dict, model, is_created: bool, request: Request) -> None:
        """Срабатывает при создании или редактировании товара"""
        file = data.get("image_url")
        
        if file and hasattr(file, "filename") and file.filename:
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            
            ext = os.path.splitext(file.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"
            file_path = os.path.join(UPLOAD_DIR, filename)
            
            # Сохраняем файл на жесткий диск
            with open(file_path, "wb") as f:
                f.write(file.file.read())
                
            data["image_url"] = f"/static/uploads/{filename}"
        else:
            if not is_created:
                data.pop("image_url", None)
            else:
                data["image_url"] = None

    async def on_model_delete(self, model, request: Request) -> None:
        """Срабатывает при удалении товара: зачищаем файлы с диска"""
        if model.image_url and model.image_url.startswith("/static/uploads/"):
            filename = model.image_url.replace("/static/uploads/", "")
            file_path = os.path.join(UPLOAD_DIR, filename)
            if os.path.exists(file_path):
                os.remove(file_path)