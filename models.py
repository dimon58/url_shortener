import logging

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import sqltypes

from configs import URL_LENGTH
from db import BaseModel
from utils import get_random_ascii_seq

logger = logging.getLogger(__name__)


class ShortUrl(BaseModel):
    short_path: Mapped[str] = mapped_column(sqltypes.VARCHAR(8), index=True)
    full_url: Mapped[str] = mapped_column(sqltypes.String)
    meta: Mapped[dict] = mapped_column(sqltypes.JSON, default=dict)

    @classmethod
    async def get_full_url(cls, db_session: AsyncSession, short_path: str):
        # noinspection PyTypeChecker
        stmt = select(cls).where(cls.short_path == short_path)
        return await db_session.scalar(stmt)

    @classmethod
    async def exists(cls, db_session: AsyncSession, short_path: str) -> bool:
        # noinspection PyTestUnpassedFixture
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
    short_path: Mapped[str] = mapped_column(sqltypes.VARCHAR(8))

    query_params: Mapped[dict] = mapped_column(sqltypes.JSON, default=dict)
    headers: Mapped[dict] = mapped_column(sqltypes.JSON, default=dict)
    cookies: Mapped[dict] = mapped_column(sqltypes.JSON, default=dict)
    success: Mapped[bool] = mapped_column(sqltypes.Boolean)

    # Распаршенный User-Agent
    # Устройство
    user_agent_device_family: Mapped[str] = mapped_column(
        doc="Device family", default=""
    )
    user_agent_device_brand: Mapped[str] = mapped_column(doc="Device brand", default="")
    user_agent_device_model: Mapped[str] = mapped_column(doc="Device model", default="")

    # Операционная система
    user_agent_os_family: Mapped[str] = mapped_column(
        doc="Operating system family", default=""
    )
    user_agent_os_version: Mapped[str] = mapped_column(
        doc="Operating system version", default=""
    )

    # Браузер
    user_agent_browser_family: Mapped[str] = mapped_column(
        doc="Browser family", default=""
    )
    user_agent_browser_version: Mapped[str] = mapped_column(
        doc="Browser version", default=""
    )

    # Кем является клиент
    user_agent_is_pc: Mapped[bool] = mapped_column(
        doc='whether user agent is identified to be running a traditional "desktop" OS (Windows, OS X, Linux)',
        default=False,
    )
    user_agent_is_mobile: Mapped[bool] = mapped_column(
        doc=(
            "whether user agent is identified as a mobile phone "
            "(iPhone, Android phones, Blackberry, Windows Phone devices etc)"
        ),
        default=False,
    )
    user_agent_is_tablet: Mapped[bool] = mapped_column(
        doc="whether user agent is identified as a tablet device (iPad, Kindle Fire, Nexus 7 etc)",
        default=False,
    )
    user_agent_is_touch_capable: Mapped[bool] = mapped_column(
        doc="whether user agent has touch capabilities",
        default=False,
    )
    user_agent_is_bot: Mapped[bool] = mapped_column(
        doc="whether user agent is a search engine crawler/spider",
        default=False,
    )
    user_agent_is_email_client: Mapped[bool] = mapped_column(
        doc="whether user agent is a email client",
        default=False,
    )
