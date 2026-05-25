from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Text

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