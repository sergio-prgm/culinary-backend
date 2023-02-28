from fastapi import HTTPException, Query, APIRouter, Depends
from typing import Union
from data.schemas import Recipe, RecipeCreate
from dependencies.db import get_db
from sqlalchemy.orm import Session
from utils import sql_utils

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"]
)


# ✅ -> /recipes?user-id=2
# ✅ -> /recipes
# Think more about 'exclude_unset' and all that
# Can make the return more concise but I don't know if it is better


@router.post("/{user_id}", response_model=Recipe)
def create_recipe(user_id: int, recipe: RecipeCreate, db: Session = Depends(get_db)):
    '''
    Creates a new recipe and links it to the correspondng user

    🔑
    Has to be authorized
    '''
    # Check if user_id exists
    user_db = sql_utils.get_user(db, user_id)
    if not user_db:
        raise HTTPException(status_code=400, detail="user_id doesn't exist.")
    return sql_utils.create_recipe(db=db, recipe=recipe, user_id=user_id)


@router.get("", response_model=list[Recipe])
def read_recipes(
    skip: Union[int, None] = 0,
    limit: Union[int, None] = 100,
    db: Session = Depends(get_db),
    user_id: Union[int, None] = Query(default=None, alias="user-id")
):
    '''
    Read all recipes within a limited interval (useful for eventual pagination)

    A user id can be provided (?user-id=id) to only read recipes from that user
    '''
    if user_id:
        user_db = sql_utils.get_user(db, user_id)
        if not user_db:
            raise HTTPException(
                status_code=400, detail=f"User with user_id={user_id} does not exist.")
        recipes = sql_utils.get_recipes_by_user_id(
            db=db, user_id=user_id, skip=skip, limit=limit)
    else:
        recipes = sql_utils.get_recipes(db=db, skip=skip, limit=limit)
    return recipes


@router.get("/{recipe_id}", response_model=Recipe)
def read_recipe_by_id(recipe_id: int, db: Session = Depends(get_db)):
    '''
    Retrieve a recipe from its id
    '''
    recipe = sql_utils.get_recipe_by_id(db=db, recipe_id=recipe_id)
    if not recipe:
        raise HTTPException(
            status_code=404, detail=f"Recipe with id {recipe_id} not found")
    return recipe

# [ ] Update and delete recipe (with JWT and all that)
