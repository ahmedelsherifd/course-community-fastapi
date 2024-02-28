from sqlalchemy.orm import Session
from . import models
from . import schemas
from .auth_utils import get_password_hash, verify_password


def get_questions(db: Session):
    return db.query(models.Question).all()


def create_question(db: Session, **data):
    question = models.Question(**data)
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def get_question(db: Session, pk):
    return db.get(models.Question, pk)


def create_user(db: Session, password=None, **data):
    hashed_password = get_password_hash(password)
    user = models.User(**data, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, username):
    return db.query(models.User).filter_by(username=username).one_or_none()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
