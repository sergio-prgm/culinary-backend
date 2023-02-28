from typing import Union
from pydantic import BaseModel


class RecipeBase(BaseModel):
    title: str
    description: str
    servings: str
    images: str


class RecipeCreate(RecipeBase):
    pass


class Recipe(RecipeBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


# class UserDB(UserBase):
#     id: int
#     hashed_password: str
#     recipes: list[Recipe]


class User(UserBase):
    id: int
    recipes: list[Recipe] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
