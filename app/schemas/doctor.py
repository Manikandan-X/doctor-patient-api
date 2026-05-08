from pydantic import BaseModel

class DoctorBase(BaseModel):
    name: str
    specialization: str
    email: str

class DoctorCreate(DoctorBase):
    pass

class DoctorResponse(DoctorBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True