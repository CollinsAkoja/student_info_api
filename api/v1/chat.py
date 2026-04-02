# api/v1/chat.py
from fastapi import APIRouter, HTTPException
from schemas.chat import ChatQuery
from utils.openai_client import query_student_data_natural_language

router = APIRouter(prefix="/chat", tags=["AI Chatbot"])

@router.post("/query-student-data")
def query_student_data(chat_query: ChatQuery):
    """
    Query student data using natural language via AI chatbot.
    """
    try:
        result = query_student_data_natural_language(chat_query.query)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")