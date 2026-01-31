def get_db():
    from app import SessionLocal

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
