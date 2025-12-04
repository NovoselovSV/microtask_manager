from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

origins = [
    'http://localhost',
    'http://localhost:8080',
    'http://localhost:8000',
    'http://localhost:3000',
    'http://localhost:5173',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(tasks.router)
app.include_router(sse.router)
app.include_router(rabbit_router)
