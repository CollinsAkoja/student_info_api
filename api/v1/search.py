# api/v1/search.py
from fastapi import APIRouter, Query
from typing import List
from schemas.student import StudentResponse
from utils import json_storage

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/students", response_model=List[StudentResponse])
def search_students(
    q: str = Query(..., description="Search query for name, email, or major"),
):
    # Reuse the get_students function with the search parameter
    students_data = json_storage.get_students(search=q)
    return [StudentResponse(**student) for student in students_data]