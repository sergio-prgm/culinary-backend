from sqlalchemy.orm import Session
# from sqlalchemy import select

from dependencies.dependencies import get_password_hash
from data import models, schemas


def get_user(db: Session, user_id: int):
    '''
    Performs a SQL
    SELECT * FROM Users WHERE user.id = user_id
    '''
    # User = models.User
    # stmt = select(User).where(User.id == user_id)
    # return db.scalars(stmt).first()
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    '''
    Performs a SQL
    SELECT * FROM Users WHERE user.email == email
    '''
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    '''
    Performs a SQL
    SELECT * FROM Users
    '''
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    '''
    Performs SQL
    INSERT INTO Users
    VALUES (user.username, user.email...)
    '''
    # Use password hash thing
    print(user)
    # fake_hashed_password = user.password + "almost"
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email,
                          hashed_password=hashed_password,
                          username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_recipes(db: Session, skip: int = 0, limit: int = 100):
    '''
    Performs a SQL
    SELECT * FROM Recipes
    '''
    return db.query(models.Recipe).offset(skip).limit(limit).all()


def get_recipe_by_id(db: Session, recipe_id: int):
    '''
    Performs a SQL
    SELECT * FROM Recipes
    '''
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()


def get_recipes_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 0):
    '''
    Perfoms a SQL
    SELECT * FROM Recipes WHERE recipe.owner_id == user.id
    '''
    return db.query(models.Recipe).filter(models.Recipe.owner_id == user_id).offset(skip).limit(limit).all()


def create_recipe(db: Session, recipe: schemas.RecipeCreate, user_id: int):
    '''
    Performs SQL

    INSERT INTO Recipes

    VALUES (recipe.title, recipe.description...)
    '''
    db_recipe = models.Recipe(**recipe.dict(), owner_id=user_id)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe
