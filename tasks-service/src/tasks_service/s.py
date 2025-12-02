import os
from configs.settings import Settings
if __name__ == "__main__":
    print(os.getenv('TASKS_USER_SERVICE__HOST'))
    s = Settings()
    print(s.user_service.dsn)
    print(s.user_service.host)
    print(s.debug)
    print(s.db.dsn)
