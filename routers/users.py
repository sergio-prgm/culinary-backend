# from datetime import timedelta

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from data.schemas import Token, User, UserCreate
from dependencies.db import get_db
from dependencies.dependencies import authenticate_user, create_access_token
from dependencies.env import ACCESS_TOKEN_EXPIRE_MINUTES
from dependencies.users import get_current_user
from utils import sql_utils

router = APIRouter(
    prefix='',
    tags=['users']
)


@router.get("/users/me", response_model=User, tags=["OAuth2"])
def read_users_me(current_user: User = Depends(get_current_user)):
    '''
    Checks if the provided user exists checking if the token is valid

    The dependency is in charge of throwing an exception if the token is incorrect
    '''
    return current_user


@router.post("/token", response_model=Token, tags=["OAuth2"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    '''
    Uses the token_url to authenticate the user.

    Throws exception if the user doesn't exist or if the password is incorrect.
    '''
    # [ ] Check if form_data.username is email or username and use the correct method
    user = authenticate_user(
        db=db, user_email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            # In the OAuth2 spec
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # {"sub": user.id, "username": user.username, "email": user.email}
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username, "email": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    '''
    Checks if user.email already exists -> raises Exception

    Creates the new User in the db
    '''
    # check username is unique
    db_user = sql_utils.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return sql_utils.create_user(db, user)


@router.get("/users", response_model=list[User], deprecated=True)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    '''
    Gets all the user within skip - limit
    '''
    users = sql_utils.get_users(db, skip, limit)
    return users


@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    '''
    Gets user information for user_id
    '''
    # [ ] Get information (user_id) from token, or headers not query params
    db_user = sql_utils.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# [ ] Update and delete user (previously authenticated)
'''
@router.put("/users/{user_id}", response_model=User)
def update_user(user_int: int, {{I dont know}} db: Session = Depends(get_db))
'''
