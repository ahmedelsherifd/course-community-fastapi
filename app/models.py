from .database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(index=True)
    username: Mapped[str] = mapped_column(index=True)
    hashed_password: Mapped[str] = mapped_column()
