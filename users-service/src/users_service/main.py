from fastapi import FastAPI

from configs.settings import Settings
from web import users

settings = Settings()

app = FastAPI(debug=settings.debug, root_path='/api/v1')

app.include_router(users.router)
