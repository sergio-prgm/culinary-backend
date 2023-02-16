from fastapi import APIRouter, Query, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Union

from schemas import UserBase, UserDB


router = APIRouter(
    prefix='/users',
    tags=['users']
)


fake_users_db = {
    "manuel": {
        "id": 0,
        "username": "manuel",
        "email": "manuel@manu.com",
        "hashed_password": "secretmanuel"
    },
    "alice": {
        "id": 1,
        "username": "alice",
        "email": "alice@uni.com",
        "hashed_password": "secretalice"
    },
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_hash_password(password: str):
    return "secret" + password


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserDB(**user_dict)


def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            # headers www-authenticate in spec
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    '''
    Uses the token_url to authenticate the user
    Throws exception if the user doesn't exist or if the password is incorrect
    '''
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    user = UserDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
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
