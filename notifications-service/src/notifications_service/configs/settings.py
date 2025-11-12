from pydantic import BaseModel
from pydantic_settings import BaseSettings


class DBSettings(BaseModel):
    dialect: str = 'postgresql'
    driver: str = 'asyncpg'
    name: str = 'notifications'
    username: str = 'general_user'
    password: str = 'general_user_pass'
    host: str = 'localhost'
    port: int = 5432

    @property
    def dsn(self):
        return (f'{self.dialect}+{self.driver}://'
                f'{self.username}:{self.password}'
                f'@{self.host}:{self.port}/{self.name}')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter='__')

    debug: bool = True
    user_secret: str = 'SECRET'
    db: DBSettings = DBSettings()
