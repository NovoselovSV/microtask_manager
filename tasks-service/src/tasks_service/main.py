from fastapi import FastAPI

from configs.settings import Settings

settings = Settings()

app = FastAPI(debug=settings.debug, root_path='/tasks/v1')
