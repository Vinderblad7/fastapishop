from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from typing import Annotated
from src.config import settings
from src.database import get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
