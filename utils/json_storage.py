# utils/json_storage.py
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from config import settings

def load_students_from_file() -> List[Dict[str, Any]]:
    """Loads the student list from the JSON file."""
    if not os.path.exists(settings.STUDENT_DATA_FILE):
        # If the file doesn't exist, create it with an empty list
        save_students_to_file([])
        return []
    try:
        with open(settings.STUDENT_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {settings.STUDENT_DATA_FILE}. Starting with empty list.")
        return [] # Return empty list if file is corrupted

def save_students_to_file(students: List[Dict[str, Any]]) -> None:
    """Saves the student list to the JSON file."""
    with open(settings.STUDENT_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(students, f, indent=2, default=str) # default=str handles datetime serialization

def get_next_id(students: List[Dict[str, Any]]) -> int:
    """Gets the next available ID based on the highest existing ID."""
    if not students:
        return 1
    return max(student['id'] for student in students) + 1

def get_students(search: str = "", major_filter: str = "", year_filter: int = 0, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    """Retrieves students from the file, applying filters and pagination."""
    students = load_students_from_file()

    # Apply filters
    filtered_students = []
    for student in students:
        match = True
        if search:
            search_lower = search.lower()
            if not (search_lower in student['first_name'].lower() or
                    search_lower in student['last_name'].lower() or
                    search_lower in student['email'].lower() or
                    search_lower in student['major'].lower()):
                match = False
        if match and major_filter and student['major'] != major_filter:
            match = False
        if match and year_filter and student['year_level'] != year_filter:
            match = False

        if match:
            filtered_students.append(student)

    # Apply pagination
    start_index = skip
    end_index = skip + limit
    paginated_students = filtered_students[start_index:end_index]

    return paginated_students

def get_student_by_id(student_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves a single student by ID."""
    students = load_students_from_file()
    for student in students:
        if student['id'] == student_id:
            return student
    return None

def create_student(student_data: Dict[str, Any]) -> Dict[str, Any]:
    """Creates a new student record in the file."""
    students = load_students_from_file()
    new_id = get_next_id(students)
    student_to_add = student_data.copy() # Avoid modifying the original dict
    student_to_add['id'] = new_id
    student_to_add['enrollment_date'] = datetime.utcnow().isoformat() + "Z" # Add timestamp

    students.append(student_to_add)
    save_students_to_file(students)
    return student_to_add

def update_student(student_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Updates an existing student record."""
    students = load_students_from_file()
    for i, student in enumerate(students):
        if student['id'] == student_id:
            # Update the student record with new data
            updated_student = student.copy()
            updated_student.update(update_data)
            students[i] = updated_student
            save_students_to_file(students)
            return updated_student # Return the updated record
    return None # Return None if student not found

def delete_student(student_id: int) -> bool:
    """Deletes a student record."""
    students = load_students_from_file()
    original_len = len(students)
    # Filter out the student with the given ID
    students[:] = [student for student in students if student['id'] != student_id]
    
    if len(students) < original_len:
        save_students_to_file(students)
        return True # Successfully deleted
    return False # Student not found