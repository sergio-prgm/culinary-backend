from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas import UserBase, UserDB


# provides a url(/token) to uthenticate a user-password and retrieve a token
# This leverages the password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


'''
The auth dependency checks if there's a Bearer Authorization
in the Header of the request
It automatically throws a 401 if Bearer or Authorization are not present

@app.put("/recipes")
async def post_recipe(token: str = Depends(oauth2_scheme)):
    return {"token": token}

'''

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user

'''
@app.get("/users/me")
async def read_users(current_user: UserBase = Depends(get_current_user)):
    return current_user
'''

