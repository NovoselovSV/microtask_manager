from faststream.rabbit.fastapi import RabbitRouter

from configs.settings import Settings

settings = Settings()

rabbit_router = RabbitRouter(settings.rabbit.dsn)
