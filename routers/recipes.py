from fastapi import HTTPException, Query, APIRouter
from typing import Union
from schemas import BaseRecipe, Recipe

router = APIRouter()

RECIPE_COLLECTION = [
    Recipe(user_id=1, title="Mashed potatoes", images=[],
           description="The best easy mashed potatoes to accompany any steak or fish.", id=0, servings=4,),
    Recipe(user_id=0, title="Boeuf bourgignon", images=[],
           description="Rich, flavourful, excessive... The meal of your dreams,", id=1, servings=4),
    Recipe(user_id=0, title="Fish and chips", images=[],
           description="If brits can do it, you can too (and even better).", id=2, servings=4, )
]

# ✅ -> /recipes?user-id=2
# ✅ -> /recipes
# Think more about 'exclude_unset' and all that
# Can make the return more concise but I don't know if it is better
@router.get("/recipes")
async def get_recipes(user_id: Union[int, None] = Query(default=None, alias="user-id")) -> list[Recipe]:
    if user_id:
        result = [
            recipe for recipe in RECIPE_COLLECTION if recipe.user_id == user_id]
        if len(result) > 0:
            return result
        else:
            raise HTTPException(
                404, f"{user_id} not found or doesn't have any recipes added.")
    return RECIPE_COLLECTION


# ✅ -> /recipes?user-id=2
# ❌ -> /recipes?user-id=2
@router.post("/recipes")
async def add_recipe(recipe: BaseRecipe, user_id: int = Query(alias="user-id")):
    # Validate that the title is unique
    # probably with db
    if not user_id:
        raise HTTPException(
            404, "The user is missing. This is a blatant error!")
    new_id = len(
        RECIPE_COLLECTION)
    return_recipe = Recipe(title=recipe.title, description=recipe.description,
                           servings=recipe.servings, id=new_id, user_id=user_id, images=recipe.images)
    print(return_recipe)
    # recipe.id = len(RECIPE_COLLECTION)
    # recipe.user_id = user_id
    RECIPE_COLLECTION.append(return_recipe)
    return {"status": "ok", "recipe": return_recipe}


# ✅ -> /recipes/:recipe-id
@router.get("/recipes/{recipe_id}")
async def get_recipe_by_id(recipe_id: int) -> Recipe:
    if recipe_id >= len(RECIPE_COLLECTION):
        raise HTTPException(status_code=404, detail="Recipe not found")

    return RECIPE_COLLECTION[recipe_id]

