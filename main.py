# main.py
from fastapi import FastAPI
from api.v1 import students, search, chat # Import your API routers

app = FastAPI(title="Student Information System API (JSON)")

# Include the API routes
app.include_router(students.router, prefix="/api/v1", tags=["Students"])
app.include_router(search.router, prefix="/api/v1", tags=["Search"])
app.include_router(chat.router, prefix="/api/v1", tags=["AI Chatbot"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Information System API"}
