from datetime import date
from pydantic import BaseModel, Field


class AppointmentBase(BaseModel):
    doctor_id: int
    patient_id: int

    # Automatically shows date format validation
    # Default = today's date
    appointment_date: date = Field(default_factory=date.today)


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentResponse(AppointmentBase):
    id: int
    status: str

    class Config:
        from_attributes = True