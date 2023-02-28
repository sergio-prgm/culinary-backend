from fastapi import FastAPI
from routers import users, recipes

from dependencies.dependencies import *
from data import models
from data.db import engine

from fastapi.middleware.cors import CORSMiddleware

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = [
    "http://localhost:3000/",
    "http://localhost:3000",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(users.router)
app.include_router(recipes.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# [x] File structure
# [x] Hashing password
# [x] JWT handling (cookies¿?)

# [x] CORS
# [x] SQL (supabase vs bit.io + cloudinary)
# [ ] Error handling/middleware
