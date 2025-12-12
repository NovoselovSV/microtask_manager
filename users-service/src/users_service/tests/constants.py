from uuid import UUID


BASE_URL = '/api/users'
BASE_API_VERSION = 'v1'
USER_UPDATE_QUEUE = 'user.update'
FIRST_USER_DATA = {
    'id': UUID('{12345678-1234-5678-1234-567812345678}'),
    'email': 'first_user@test.com',
    'is_active': True,
    'is_superuser': False,
    'is_verified': False}
SECOND_USER_DATA = {
    'id': UUID('{87654321-4321-8765-4321-876543218765}'),
    'email': 'second_user@test.com',
    'is_active': True,
    'is_superuser': False,
    'is_verified': False}
