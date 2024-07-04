from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class ConnectionPool:
    _instance = None

    def __init__(self, pool_size=5):
        self.engine = create_engine('mysql+mysqlconnector://root:root@localhost/library', pool_size=pool_size)
        self.Session = sessionmaker(bind=self.engine)

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def get_session(self):
        return self.Session()