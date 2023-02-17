from datetime import timedelta, datetime
from typing import Union, Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError

from schemas import UserDB, TokenData
from mock import fake_users_db

# Variables for the JWT
# echo "SECRET_KEY = \"$(openssl rand -hex 32)\"" >> dependencies.py
# SECRET_KEY = "be66c32bd800057d5fb323143fda099f2b8410efa808e70f4c31055dbb7ab567"
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
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
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        # headers www-authenticate in spec
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="JWT appears to be expired! Try logging in again.",
            headers={"WWW-Authenticate": "Bearer", "X-action": "retry-login"}
        )
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserDB(**user_dict)


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
