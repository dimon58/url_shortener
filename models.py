import logging

from sqlalchemy import Column, select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import sqltypes

from configs import URL_LENGTH
from db import BaseModel
from utils import get_random_ascii_seq

logger = logging.getLogger(__name__)


class ShortUrl(BaseModel):
    short_path: Mapped[str] = Column(sqltypes.VARCHAR(8), nullable=False, index=True)
    full_url: Mapped[str] = Column(sqltypes.String, nullable=False)
    meta: Mapped[dict] = Column(sqltypes.JSON, default=dict)

    @classmethod
    async def get_full_url(cls, db_session: AsyncSession, short_path: str):
        stmt = select(cls).where(cls.short_path == short_path)
        return await db_session.scalar(stmt)

    @classmethod
    async def exists(cls, db_session: AsyncSession, short_path: str) -> bool:
        stmt = exists().select_from(cls).where(cls.short_path == short_path).select()
        return await db_session.scalar(stmt)

    @classmethod
    async def generate(cls, db_session: AsyncSession, full_url: str, meta: dict) -> str:
        while True:
            path = get_random_ascii_seq(URL_LENGTH)
            if not await ShortUrl.exists(db_session, path):
                new_short_url = cls(
                    short_path=path,
                    full_url=full_url,
                    meta=meta,
                )
                db_session.add(new_short_url)

                return path

            logger.warning("Generated existing url")


class Click(BaseModel):
    short_path: Mapped[str] = Column(sqltypes.VARCHAR(8), nullable=False)

    query_params: Mapped[dict] = Column(sqltypes.JSON, default=dict)
    headers: Mapped[dict] = Column(sqltypes.JSON, default=dict)
    cookies: Mapped[dict] = Column(sqltypes.JSON, default=dict)
    success: Mapped[bool] = Column(sqltypes.Boolean)
