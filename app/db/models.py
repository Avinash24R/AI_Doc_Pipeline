
from datetime import datetime
from datetime import timezone
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Text, DateTime ,Float

from app.db.database import Base


class Document(Base):

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
   
    filename: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    filepath: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String,
        default="PENDING"
    )

    extracted_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    user_email: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    queued_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    queue_wait_ms: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    execution_ms: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    end_to_end_ms: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    celery_task_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        
    )

