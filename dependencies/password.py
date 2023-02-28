
from passlib.context import CryptContext

# Password hashing:
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    '''
    Checks if the provided password matches the hashed password

    (Used for authentication purposes)
    '''
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    '''
    Creates the hashed password to store in the database

    (Used for creating a new user)
    ✅
    '''
    return pwd_context.hash(password)
