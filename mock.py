from data.schemas import Recipe


fake_users_db = {
    "manuel": {
        "id": 0,
        "username": "manuel",
        "email": "manuel@manu.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
    },
    "alice": {
        "id": 1,
        "username": "alice",
        "email": "alice@uni.com",
        "hashed_password": "secretalice"
    },
}

RECIPE_COLLECTION = [
    Recipe(user_id=1, title="Mashed potatoes", images="",
           description="The best easy mashed potatoes to accompany any steak or fish.", id=0, servings="4-6",),
    Recipe(user_id=0, title="Boeuf bourgignon", images="",
           description="Rich, flavourful, excessive... The meal of your dreams,", id=1, servings="4-6"),
    Recipe(user_id=0, title="Fish and chips", images="",
           description="If brits can do it, you can too (and even better).", id=2, servings="4-6", )
]
