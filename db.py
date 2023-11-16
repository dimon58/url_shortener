from datetime import datetime

from sqlalchemy import Column, func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, declarative_base, declared_attr
from sqlalchemy.sql import sqltypes

import configs

db_engine = create_async_engine(url=configs.DB_URL)
async_session_maker = async_sessionmaker(bind=db_engine, autocommit=False, expire_on_commit=False)

Base = declarative_base()


class BaseModel(Base):
    """
    Абстрактная базовая модель с id и датой добавления
    """

    __abstract__ = True

    id: Mapped[int] = Column(
        sqltypes.Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )

    date: Mapped[datetime] = Column(
        sqltypes.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),  # pylint: disable=not-callable
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id!r})>"

    # noinspection PyMethodParameters,SpellCheckingInspection
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return cls.__name__.lower()
