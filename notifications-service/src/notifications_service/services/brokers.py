from faststream.rabbit import RabbitBroker
from configs.settings import Settings

settings = Settings()

rabbit_broker = RabbitBroker(settings.rabbit.dsn)
