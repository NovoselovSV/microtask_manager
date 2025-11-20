import httpx
import jwt
from fastapi import Header, HTTPException

from configs.settings import Settings

settings = Settings()


class UserService:

    def __init__(self, raw_token: str):
        self.raw_token: str = raw_token
        self.id: str = self.get_user_id_from_token(self.raw_token)

    async def get_info(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f'{settings.user_service.dsn}/me',
                headers={'Authorization': f'Bearer {self.raw_token}'})
            response.raise_for_status()
            return response.json()

    @classmethod
    def get_current_user(
            cls,
            authorization: str = Header(...)):
        return cls(authorization)

    @staticmethod
    def get_user_id_from_token(token: str):
        try:
            token = token.split(' ')[1]
            user_id = jwt.decode(token, options={'verify_signature': False})
            return user_id

        except IndexError:
            raise HTTPException(status_code=400,
                                detail='Invalid Authorization header format')
        except jwt.DecodeError:
            raise HTTPException(status_code=400, detail='Invalid JWT token')
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f'Unexpected error: {
                    str(error)}')
