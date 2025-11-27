from contextlib import asynccontextmanager

from fastapi import FastAPI

from configs.settings import Settings
from faststream_app import rabbit_router
from web import rabbit_receivers, sse, tasks # noqa F401

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit_router.broker.connect()
    yield
    await rabbit_router.broker.close()

app = FastAPI(debug=settings.debug, root_path='/tasks', lifespan=lifespan)

app.include_router(tasks.router)
app.include_router(sse.router)
app.include_router(rabbit_router)
