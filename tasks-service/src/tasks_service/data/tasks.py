import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from p_database.db import Base


class Task(Base):

    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    description: Mapped[str] = mapped_column(Text, default='')
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now)
    done: Mapped[Optional[bool]]
    done_dt: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True)
    final_dt: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True)
    creator_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )
