import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from dependencies import engine
from model.base import Base

from router.invocations_router import router as invocations_router
from router.profiles_router import router as profiles_router
from router.invocation_stop_requests_router import (
    router as invocation_stop_requests_router
)
from router.conversations_router import router as conversations_router
from router.documents_stored_router import router as documents_stored_router
from router.documents_embedded_router import (
    router as documents_embedded_router
)
from router.chat_turns_router import router as chat_turns_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def create_tables():
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_tables()
    yield
    engine.dispose()


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
app.include_router(invocation_stop_requests_router)
app.include_router(conversations_router)
app.include_router(documents_stored_router)
app.include_router(documents_embedded_router)
app.include_router(chat_turns_router)


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
