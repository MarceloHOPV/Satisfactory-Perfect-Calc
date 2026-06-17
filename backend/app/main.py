import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import buildings, items, recipes, calculator, saved_productions

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating database tables…")
    Base.metadata.create_all(bind=engine)
    logger.info("Database ready.")
    yield


app = FastAPI(
    title="Satisfactory Perfect Calc",
    description="Production-line optimizer for the game Satisfactory",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(buildings.router, prefix="/api/v1")
app.include_router(items.router, prefix="/api/v1")
app.include_router(recipes.router, prefix="/api/v1")
app.include_router(calculator.router, prefix="/api/v1")
app.include_router(saved_productions.router, prefix="/api/v1")


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}
