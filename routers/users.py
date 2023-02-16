from fastapi import APIRouter, Query, HTTPException
from typing import Union

from schemas import UserBase


router = APIRouter(
    prefix='/users',
    tags=['users']
)

users = [
    UserBase(username='Juan Fernando', email='juan@fernando.com', id=3),
    UserBase(username='Elena María', email='elena@maria.es', id=4)
]


@router.get("")
async def read_users(name: Union[str, None] = Query(default=None, alias='name')) -> list[UserBase]:
    if name:
        result = list(filter(lambda x: x.username == name, users))
        if len(result) > 0:
            return result
        raise HTTPException(404, f"User: {name} not found in our db.")
    return users
