import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.vars import DATABASE_URL
from model.base import Base
from router.invocations_router import router as invocations_router
from router.profiles_router import router as profiles_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def create_tables():
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")


# The logic before `yield` runs on app startup, and any 
# logic after `yield` runs on app shutdown.
@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Starting up Database Service...")

    logger.debug(f"Creating tables with DATABASE_URL: {DATABASE_URL}")
    create_tables()
    logger.info("Tables created.")

    yield

    logger.info("Shutting down Database Service...")


app = FastAPI(
    title="Database Service",
    description=(
        "Database service for managing graph " 
        "invocations and state",
    ),
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(invocations_router)
app.include_router(profiles_router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8003,
        reload=True,
    )
