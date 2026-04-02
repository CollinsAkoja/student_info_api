# api/v1/students.py
from fastapi import APIRouter, HTTPException, Query
from typing import List
from schemas.student import StudentResponse, StudentCreate, StudentUpdate
from utils import json_storage

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/", response_model=List[StudentResponse])
def read_students(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, le=1000, description="Maximum number of records to return"),
    search: str = Query("", description="Search term for first name, last name, email, or major"),
    major_filter: str = Query("", alias="major", description="Filter by major/course"),
    year_filter: int = Query(0, alias="year", ge=0, le=5, description="Filter by year level (1-5)"),
):
    students_data = json_storage.get_students(search=search, major_filter=major_filter, year_filter=year_filter, skip=skip, limit=limit)
    return [StudentResponse(**student) for student in students_data] # Convert dict to Pydantic model

@router.get("/{student_id}", response_model=StudentResponse)
def read_student(student_id: int):
    student_data = json_storage.get_student_by_id(student_id)
    if student_data is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return StudentResponse(**student_data)

@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate):
    # Check if email already exists
    all_students = json_storage.load_students_from_file()
    if any(s['email'] == student.email for s in all_students):
        raise HTTPException(status_code=400, detail="Student with this email already exists")
    student_dict = student.model_dump()
    created_student_data = json_storage.create_student(student_dict)
    return StudentResponse(**created_student_data)

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student_update: StudentUpdate):
    update_data = student_update.model_dump(exclude_unset=True)
    updated_student_data = json_storage.update_student(student_id, update_data)
    if updated_student_data is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return StudentResponse(**updated_student_data)

@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int):
    success = json_storage.delete_student(student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    # Return 204 No Content on successful deletion
    return