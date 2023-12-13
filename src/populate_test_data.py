import logging

from db.session import db_session
from db.init import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def populate_companies_and_users():
    from models.company import Company
    from schemas.company import CompanyCreate
    from crud.company import CRUDCompany
    from models.user import User
    from schemas.user import UserCreate
    from crud.user import CRUDUser


    company_in = CompanyCreate(
        name="Company 1",
        is_active=True,
    )
    company_obj = CRUDCompany(db_session).create(obj_in=company_in)

    user_in = UserCreate(
        username="user1",
        otp_enabled=True,
        password="user1",
        is_active=True,
        is_superuser=False,
    )
    user_obj = CRUDUser(db_session).create(obj_in=user_in, company=company_obj)
    user_obj.is_claimed = True
    db_session.add(user_obj)
    db_session.commit()

    user_in = UserCreate(
        username="user2",
        otp_enabled=True,
        password="user2",
        is_active=True,
        is_superuser=False,
    )
    user_obj = CRUDUser(db_session).create(obj_in=user_in, company=company_obj)
    user_obj.is_claimed = True
    db_session.add(user_obj)
    db_session.commit()
        

    company_in = CompanyCreate(
        name="Company 2",
        is_active=True,
    )
    company_obj = CRUDCompany(db_session).create(obj_in=company_in)

    user_in = UserCreate(
        username="user3",
        otp_enabled=True,
        password="user3",
        is_active=True,
        is_superuser=False,
    )
    user_obj = CRUDUser(db_session).create(obj_in=user_in, company=company_obj)
    user_obj.is_claimed = True
    db_session.add(user_obj)
    db_session.commit()

    

def main():
    logging.info("Creating companies...")
    populate_companies_and_users()
    logging.info("Companies data created...")


if __name__ == "__main__":
    main()