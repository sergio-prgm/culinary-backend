from data.database import SessionLocal

# Opens the db connection on each request that uses it and auto-closes


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
