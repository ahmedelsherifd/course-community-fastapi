from pydantic import BaseModel, model_validator


class Question(BaseModel):
    id: int
    name: str


class QuestionInput(BaseModel):
    name: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    name: str | None = None


class UserInput(BaseModel):
    username: str
    email: str | None = None
    name: str | None = None
    password: str
    password2: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserInput":
        pw1 = self.password
        pw2 = self.password2
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("passwords do not match")
        return self
