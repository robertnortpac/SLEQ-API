import logging

from app.db.session import db_session
from app.db.init import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init():
    init_db(db_session)

def main():
    logging.info("Creating initial data...")
    init()
    logging.info("Initial data created...")


if __name__ == "__main__":
    main()
