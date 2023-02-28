from datetime import timedelta, datetime
from typing import Union

from passlib.context import CryptContext
from jose import jwt
from dependencies.usersdeps import get_user
from dependencies.env import ALGORITHM, SECRET_KEY


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    '''
    Creates and returns JWT with provided data and expiring date
    '''
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Password hashing:
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    '''
    Checks if the provided password matches the hashed password

    (Used for authentication purposes)
    '''
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    '''
    Creates the hashed password to store in the database

    (Used for creating a new user)
    '''
    return pwd_context.hash(password)


def authenticate_user(fake_db, username: str, password: str):
    '''
    Checks if the user provided exists and verifies the password given

    If everything works correctly, it returns the user

    Used in /token
    '''
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
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
