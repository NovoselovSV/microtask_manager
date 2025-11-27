from contextlib import asynccontextmanager
from fastapi import FastAPI

from configs.settings import Settings
from web import users, sse, rabbit_receivers  # noqa F401
from faststream_app import rabbit_router

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit_router.broker.connect()
    yield
    await rabbit_router.broker.close()

app = FastAPI(debug=settings.debug, root_path='/users', lifespan=lifespan)

app.include_router(sse.router)
app.include_router(users.router)
app.include_router(rabbit_router)
