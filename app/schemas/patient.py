from pydantic import BaseModel

class PatientBase(BaseModel):
    name: str
    age: int
    phone: str
    email: str
    
class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int

    class Config:
        from_attributes = True