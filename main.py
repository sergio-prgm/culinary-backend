from fastapi import FastAPI
from routers import users, recipes
# from uuid import UUID

app = FastAPI()

app.include_router(users.router)
app.include_router(recipes.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# [x] File structure
# [ ] Hashing password
# [ ] JWT handling (cookies¿?)
# [ ] Error handling
# [ ] CORS
# [ ] SQL (supabase vs bit.io + cloudinary)
