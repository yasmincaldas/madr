from http import HTTPStatus

from fastapi import APIRouter, Depends

from madr.schemas import AuthorSchemaCreate
from madr.db import User, AsyncSession, get_async_session
from madr.models import Author

router = APIRouter(prefix='/authors', tags='authors')


T_Session = Annotated[AsyncSession, Depends(get_async_session)]
current_active_verified_user = fastapi_users.current_user(
    active=True, verified=True
)


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=AuthorSchemaCreate
)
async def add_author(
    session: T_Session,
    author: AuthorSchemaCreate,
    user: User = Depends(current_active_verified_user),
):
    new_author = Author(
        name=author.name,
    )

    session.add(new_author)
    await session.commit()
    await session.refresh(new_author)
