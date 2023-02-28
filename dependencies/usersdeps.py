from fastapi import Depends, HTTPException, status
from jose import ExpiredSignatureError, jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

from data.schemas import TokenData, User
from dependencies.env import SECRET_KEY, ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)
