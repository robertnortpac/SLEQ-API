import logging

from db.session import db_session
from db.init import init_db

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
