from fastapi import FastAPI
from routers import users, recipes
from dependencies import *
from schemas import Token
from mock import fake_users_db
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

app.include_router(users.router)
app.include_router(recipes.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    '''
    Uses the token_url to authenticate the user
    Throws exception if the user doesn't exist or if the password is incorrect
    '''
    user = authenticate_user(
        fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            # In the OAuth2 spec
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# [x] File structure
# [ ] Hashing password
# [ ] JWT handling (cookies¿?)
# [ ] Error handling
# [ ] CORS
# [ ] SQL (supabase vs bit.io + cloudinary)
