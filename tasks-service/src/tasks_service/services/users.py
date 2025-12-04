import httpx
import jwt
from fastapi import Header, HTTPException, status

from configs.settings import Settings
from data.users_schemas import UserReadSchema

settings = Settings()


class UserService:

    def __init__(self, raw_token: str):
        self.raw_token: str = raw_token
        self.id: str = self.get_user_id_from_token(self.raw_token)

    async def get_info(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f'{settings.user_service.dsn}/me',
                headers={'Authorization': self.raw_token})
            response.raise_for_status()
            return UserReadSchema(**response.json())

    @classmethod
    def get_current_user(
            cls,
            authorization: str = Header(...)):
        return cls(authorization)

    @staticmethod
    async def get_user_info_before_logic(
            authorization: str = Header(...)):
        user = UserService.get_current_user(authorization)
        return await user.get_info()

    @staticmethod
    def get_user_id_from_token(token: str):
        try:
            token = token.split(' ')[1]
            user_id = jwt.decode(token, options={'verify_signature': False})
            return user_id.get('sub')

        except IndexError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Invalid Authorization header format')
        except jwt.DecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid JWT token')
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Unexpected error: {str(error)}')
