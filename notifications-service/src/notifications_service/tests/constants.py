from datetime import datetime
from uuid import UUID


USER_CONNECTED_QUEUE = 'user.connected'
USER_DISCONNECTED_QUEUE = 'user.disconnected'
TASK_USER_QUEUE = 'task.user'
TASK_UPDATE_QUEUE = 'task.update'
TASK_END_QUEUE = 'task.end'
USER_ID = UUID('{12345678-1234-5678-1234-567812345678}').hex
SECOND_USER_ID = UUID('{87654321-4321-8765-4321-876543218765}').hex
TASK_DATA = {'id': 1,
             'final_dt': datetime(2025, 12, 1, 12, 0),
             'creator_id': USER_ID}
