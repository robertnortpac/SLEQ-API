import logging

from app.db.session import db_session
from app.utils.service_result import handle_result
from app.core.auth.security import show_otp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def populate_companies_and_users():
    from app.schemas.company import CompanyCreate
    from app.services.company import CompanyService
    from app.schemas.user import UserCreate
    from app.services.user import UserService

    from app.services.auth import AuthenticationService
    from app.schemas.auth import ClaimAccount

    sample_company_user_data = [
        {
            "name": "Company 1",
            "users": [
                {
                    "username": "user1",
                    "password": "user1",
                },
                {
                    "username": "user2",
                    "password": "user2",
                }
            ],
        },
        {
            "name": "Company 2",
            "users": [
                {
                    "username": "user3",
                    "password": "user3",
                },
            ],
        }
    ]

    for company_user_data in sample_company_user_data:
        company_in = CompanyCreate(**company_user_data)
        company_obj = handle_result(
            CompanyService(db_session).create_company(obj_in=company_in)
        )

        for user_data in company_user_data["users"]:
            user_in = UserCreate(
                username=user_data["username"],
                password=user_data["password"],
                is_active=True,
                is_superuser=False,
                otp_enabled=True,
                company_id=company_obj.id,
            )
            user_obj = handle_result(UserService(db_session).create_user(obj_in=user_in))

            claim_account = ClaimAccount(
                claim_code=user_obj.claim_code,
                password=user_data["password"],
                password_confirm=user_data["password"],
                otp=show_otp(user_obj.otp_secret),
            )
            AuthenticationService(db_session).claim_user(obj_in=claim_account)

def populate_tpas():
    from app.schemas.tpa import TpaCreate
    from app.services.tpa import TpaSevice

    sample_tpa_data = [
        {"name": "TPA 1"},
        {"name": "TPA 2"},
        {"name": "TPA 3"},
        {"name": "TPA 4"},
    ]

    for tpa_data in sample_tpa_data:
        tpa_in = TpaCreate(**tpa_data)
        TpaSevice(db_session).create_tpa(obj_in=tpa_in)


def populate_sics():
    from app.schemas.sic import SicCreate
    from app.services.sic import SicService

    sample_sic_data = [
        {"code": "0100", "description": "Random Sic 1"},
        {"code": "0200", "description": "Random Sic 2"},
        {"code": "0300", "description": "Random Sic 3"},
        {"code": "0400", "description": "Random Sic 4"},
    ]

    for sic_data in sample_sic_data:
        sic_in = SicCreate(**sic_data)
        SicService(db_session).create_sic(obj_in=sic_in)


def main():
    logging.info("Creating companies...")
    populate_companies_and_users()
    logging.info("Companies data created...")

    logging.info("Creating tpas...")
    populate_tpas()
    logging.info("TPAs data created...")

    logging.info("Creating sics...")
    populate_sics()
    logging.info("SICs data created...")


if __name__ == "__main__":
    main()
