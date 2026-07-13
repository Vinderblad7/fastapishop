from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from sqlalchemy import select

from src.database import new_session
from src.users.models import UserModel
from src.categories.models import CategoryModel
from src.users.utils import verify_password
from src.config import settings

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