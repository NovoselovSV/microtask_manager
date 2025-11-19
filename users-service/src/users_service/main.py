from fastapi import FastAPI

from configs.settings import Settings
from web import users

settings = Settings()

app = FastAPI(debug=settings.debug, root_path='/users/v1')

app.include_router(users.router)
