from fastapi import APIRouter, Depends
from schemas import UserBase
from dependencies import *

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get("/me", response_model=UserBase)
async def read_users_me(current_user: UserBase = Depends(get_current_user)):
    '''
    Checks if the provided user exists checking if the token is valid
    The dependency is in charge of throwing an exception if the token is incorrect
    '''
    return current_user


# @router.get("")
# async def read_users(name: Union[str, None] = Query(default=None, alias='name')) -> list[UserBase]:
#     if name:
#         result = list(filter(lambda x: x.username == name, users))
#         if len(result) > 0:
#             return result
#         raise HTTPException(404, f"User: {name} not found in our db.")
#     return users
