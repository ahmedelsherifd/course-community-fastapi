from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from .database import SessionLocal
from fastapi.routing import APIRoute
from . import schemas
from . import crud
from typing import Annotated
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .auth_utils import (
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    oauth2_scheme,
    ALGORITHM,
    SECRET_KEY,
)
from jose import JWTError, jwt

# from .auth_utils import oauth
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware


def custom_generate_unique_id(route: APIRoute):
    return f"{route.name}"


app = FastAPI(
    title="Auction book",
    generate_unique_id_function=custom_generate_unique_id,
)
app.add_middleware(SessionMiddleware, secret_key="!secret")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.get("/questions/", response_model=list[schemas.Question], tags=["questions"])
def get_questions(db: Session = Depends(get_db)):
    return crud.get_questions(db)


@app.post("/questions/", response_model=schemas.QuestionInput, tags=["questions"])
def create_question(input: schemas.QuestionInput, db: Session = Depends(get_db)):
    return crud.create_question(db, **input.model_dump())


@app.get("/questions/{pk}", response_model=schemas.Question, tags=["questions"])
def get_question(pk: str, db: Session = Depends(get_db)):
    return crud.get_question(db, pk)


@app.post("/token", response_model=schemas.Token, tags=["users"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schemas.User, tags=["users"])
async def read_users_me(
    current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    return current_user


@app.post("/users/", response_model=schemas.Token, tags=["users"])
def create_user(input: schemas.UserInput, db: Session = Depends(get_db)):
    user = crud.create_user(db, **input.model_dump(exclude={"password2"}))
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
