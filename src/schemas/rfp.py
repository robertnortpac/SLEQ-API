from typing import Optional
from pydantic import BaseModel, Field, field_validator
from datetime import date
from dateutil.relativedelta import relativedelta

from .base import BaseInDB


class RfpBase(BaseModel):
    group_name: str = "Test Group Name"
    address_street_1: str = "123 Test Street"
    address_street_2: Optional[str] = None
    address_city: str = "Test City"
    address_state: str = "TX"
    address_zip: str = Field("12345", min_length=5, max_length=5)
    has_claims_experience: bool = False
    has_current_coverage: bool = False
    sic_code_id: str
    tpa_id: str
    effective_date: date = date.today() + relativedelta(months=+1)

    company_id: Optional[str] = None

    @field_validator("effective_date")
    @classmethod
    def validate_effective_date(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("Effective date cannot be in the past")
        elif v > date.today() + relativedelta(months=+5):
            raise ValueError(
                "Effective date cannot be more than 5 months in the future"
            )
        return v


class RfpCreate(RfpBase):
    pass


class RfpUpdate(RfpBase):
    pass


class RfpInDBBase(BaseInDB, RfpBase):
    pass


class Rfp(RfpInDBBase):
    pass


class RfpInDB(RfpInDBBase):
    pass
