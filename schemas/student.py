# schemas/student.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    gpa: Optional[float] = None
    major: str
    year_level: int
    status: str
    address: Optional[str] = None
    phone_number: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    gpa: Optional[float] = None
    major: Optional[str] = None
    year_level: Optional[int] = None
    status: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None

class StudentResponse(StudentBase):
    id: int
    enrollment_date: datetime