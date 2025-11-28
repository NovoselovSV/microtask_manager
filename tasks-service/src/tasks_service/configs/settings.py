from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseModel):
    dialect: str = 'postgresql'
    driver: str = 'asyncpg'
    name: str = 'tasks'
    username: str = 'general_user'
    password: str = 'general_user_pass'
    host: str = 'localhost'
    port: int = 5432

    @property
    def dsn(self):
        return (f'{self.dialect}+{self.driver}://'
                f'{self.username}:{self.password}'
                f'@{self.host}:{self.port}/{self.name}')


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


class UserServiceSettings(BaseModel):
    host: str = 'localhost:8000'
    version: str = 'v1'

    @property
    def dsn(self):
        return (f'http://{self.host}/users/'
                f'{self.version}')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter='__', env_prefix='TASKS')

    debug: bool = True
    task_user_queue: str = 'task.user'
    user_connected_queue: str = 'user.connected'
    user_disconnected_queue: str = 'user.disconnected'
    task_update_queue: str = 'task.update'
    user_service: UserServiceSettings() = UserServiceSettings()
    db: DBSettings = DBSettings()
    rabbit: RabbitSettings = RabbitSettings()
