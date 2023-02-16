from typing import Union
from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    username: str
    email: str
    disabled: Union[bool, None] = None


class UserIn(BaseModel):
    username: str
    email: str
    password: str

class UserDB(UserBase):
    hashed_password: str


class User(UserBase):
    id: int


class BaseRecipe(BaseModel):
    title: str
    images: list[str]
    description: str
    servings: int


class Recipe(BaseRecipe):
    id: int
    user_id: int
