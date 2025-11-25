from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitSettings(BaseModel):
    driver: str = 'amqp'
    username: str = 'guest'
    password: str = 'guest'
    host: str = 'localhost'
    port: int = 5672

    @property
    def dsn(self):
        return (f'{self.driver}://'
                f'{self.username}:{self.password}'
                f'@{self.host}:{self.port}/')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter='__', env_prefix='TASKS')

    debug: bool = True
    rabbit: RabbitSettings = RabbitSettings()
