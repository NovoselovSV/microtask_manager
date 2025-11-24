from faststream import FastStream
from faststream.rabbit.fastapi import RabbitBroker

from configs.settings import Settings

settings = Settings()

rabbit_broker = RabbitBroker(settings.rabbit.dsn)
faststream_app = FastStream(rabbit_broker)
