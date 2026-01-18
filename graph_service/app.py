import logging

from fastapi import FastAPI

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Deep Research Graph Service")

logger.info("Starting Deep Research Graph Service initialization")
logger.info("Graph service initialized successfully")


@app.get("/health")
async def health():
    logger.debug("Health check requested")
    return {"status": "ok"}
