__all__ = [
    'router',
]

import asyncio

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from src.database.db import get_async_session


health_router = APIRouter()


@health_router.get(
    path='/healthz',
    tags=['healthz'],
    status_code=HTTP_200_OK,
)
async def health_check(
        session: AsyncSession = Depends(get_async_session),
):
    """Check api external connection."""
    async def check_service(service: str) -> None:
        try:
            if service == 'postgres':
                await session.execute(text('SELECT 1'))
        except Exception as exc:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST)

    await asyncio.gather(*[
        check_service('postgres'),
    ])

    return {'status': 'ok'}