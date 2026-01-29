from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from madr.db import User, create_db_and_tables
from madr.schemas import UserCreate, UserRead, UserUpdate
from madr.users import auth_backend, current_active_user, fastapi_users
from madr.routers import authors, books
from fastapi.responses import RedirectResponse


app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='/auth',
    tags=['auth'],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix='/auth',
    tags=['auth'],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)

app.include_router(authors.router)
app.include_router(books.router)


@app.get('/', include_in_schema=False)
async def root():
    return RedirectResponse(url='/docs')


@app.get('/authenticated-route')
async def authenticated_route(user: User = Depends(current_active_user)):
    return {'message': f'Hello {user.email}!'}
