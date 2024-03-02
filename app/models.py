from .database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, ForeignKey


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    community_id: Mapped[int] = mapped_column(ForeignKey("communities.id"))


class QuestionVote(Base):
    __tablename__ = "questions_votes"

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))


class AnswerVote(Base):
    __tablename__ = "answers_votes"

    id: Mapped[int] = mapped_column(primary_key=True)
    answer_id: Mapped[int] = mapped_column(ForeignKey("answers.id"))
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Community(Base):
    __tablename__ = "communities"

    id: Mapped[int] = mapped_column(primary_key=True)


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    community_id: Mapped[int] = mapped_column(ForeignKey("communities.id"))


class SubCommunity(Base):
    __tablename__ = "subcommunities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    community_id: Mapped[int] = mapped_column(ForeignKey("communities.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(index=True)
    username: Mapped[str] = mapped_column(index=True)
    hashed_password: Mapped[str] = mapped_column()
