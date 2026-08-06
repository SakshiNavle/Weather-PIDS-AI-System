from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AlertBase(BaseModel):
    site_name: str = Field(..., max_length=100)

    risk_level: str = Field(
        ...,
        description="LOW | MEDIUM | HIGH | SEVERE"
    )

    message: str = Field(..., max_length=255)

    is_active: bool = True


class AlertCreate(AlertBase):
    pass


class AlertUpdate(BaseModel):
    risk_level: str | None = None

    message: str | None = None

    is_active: bool | None = None


class AlertResponse(AlertBase):
    id: int

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )