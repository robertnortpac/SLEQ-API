from sqlalchemy.orm import Session
from app.models.user import User

class DBSessionContext(object):
    def __init__(self, db: Session, current_user: User = None):
        self.db = db
        self.current_user = current_user

class BaseService(DBSessionContext):
    pass