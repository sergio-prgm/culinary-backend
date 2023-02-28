from fastapi import Depends, HTTPException, status
from jose import ExpiredSignatureError, jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

from data.schemas import TokenData
from dependencies.db import get_db
from dependencies.env import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session

from utils import sql_utils


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    '''### Dependency

    Checks if the JWT is correct:
    - Has a username inside of "sub" 
    - The JWT is "decodable" using the right key and algorithm

    Returns 401 errors:
    - If the JWT is expired
    - If there is anything else wrong with the provided JWT
    - If there is a user in the JWT but it doesn't exist in the db

    Returns the user 
    '''
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        # headers www-authenticate in spec
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("username")
        user_id = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, id=user_id)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="JWT appears to be expired! Try logging in again.",
            headers={"WWW-Authenticate": "Bearer", "X-action": "retry-login"}
        )
    except JWTError:
        raise credentials_exception
    user = sql_utils.get_user(db=db, user_id=token_data.id)
    # user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

""" 
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)
"""
