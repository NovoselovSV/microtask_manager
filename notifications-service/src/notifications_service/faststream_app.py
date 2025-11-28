from contextlib import asynccontextmanager
from faststream import FastStream

from configs.settings import Settings
from services.brokers import rabbit_broker
from web import rabbit_receivers  # noqa F401
from schedulers import scheduler

settings = Settings()


@asynccontextmanager
async def lifespan():
    scheduler.start()
    yield
    scheduler.shutdown(wait=False)

faststream_app = FastStream(rabbit_broker, lifespan=lifespan)
