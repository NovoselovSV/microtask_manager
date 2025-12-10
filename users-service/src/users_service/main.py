from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from configs.settings import Settings
from web import users, sse, rabbit_receivers  # noqa F401
from faststream_app import rabbit_router

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit_router.broker.connect()
    yield
    await rabbit_router.broker.close()

app = FastAPI(debug=settings.debug, root_path='/api/users', lifespan=lifespan)

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

app.include_router(sse.router)
app.include_router(users.router)
app.include_router(rabbit_router)
