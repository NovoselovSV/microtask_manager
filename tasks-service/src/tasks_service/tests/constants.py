from datetime import datetime
from uuid import UUID

BASE_URL = '/api/tasks'
BASE_API_VERSION = 'v1'
TASK_END_QUEUE = 'task.end'
FIRST_USER_DATA_ID = UUID('{12345678-1234-5678-1234-567812345678}')
FIRST_USER_DATA = {
    'id': FIRST_USER_DATA_ID,
    'is_active': True}
SECOND_USER_DATA_ID = UUID('{87654321-4321-8765-4321-876543218765}')
SECOND_USER_DATA = {
    'id': SECOND_USER_DATA_ID,
    'is_active': True}
FIRST_TASK_FIRST_USER_DATA = {
    'id': 1,
    'created_at': datetime(2025, 1, 1, 12, 0),
    'done': False,
    'done_dt': None,
    'creator_id': FIRST_USER_DATA_ID,
    'description': 'simple task',
    'final_dt': datetime(2025, 1, 1, 13, 0)
}
