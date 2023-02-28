from datetime import timedelta, datetime
from typing import Union

from jose import jwt
from dependencies.env import ALGORITHM, SECRET_KEY
from sqlalchemy.orm import Session

from dependencies import password as pwd
from utils import sql_utils


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    '''
    Creates and returns JWT with provided data and expiring date.

    It doesn't have the responsibility of the data that is put into it.
    '''
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(db: Session, user_email: str, password: str):
    '''
    Checks if the user id provided exists and verifies the password given

    If everything works correctly, it returns the user

    Used in /token
    '''
    # user = get_user(db, username)
    user = sql_utils.get_user_by_email(db=db, email=user_email)
    if not user:
        return False
    if not pwd.verify_password(password, user.hashed_password):
        return False
    return user


'''
The auth dependency checks if there's a Bearer Authorization
in the Header of the request
It automatically throws a 401 if Bearer or Authorization are not present

@app.put("/recipes")
async def post_recipe(token: str = Depends(oauth2_scheme)):
    return {"token": token}

@app.get("/users/me")
async def read_users(current_user: UserBase = Depends(get_current_user)):
    return current_user
'''
