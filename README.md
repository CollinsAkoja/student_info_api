# Student Information System API (JSON)

This is a FastAPI-based REST API for managing student records using a JSON file for storage, featuring CRUD operations, search, pagination, filtering, and an AI-powered chatbot for natural language queries.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd student_info_api
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/Scripts/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    *   Create a `.env` file in the project root.
    *   Add your OpenAI API key:
        ```init
        OPENAI_API_KEY="API_KEY"
        <!-- api_key = youIzaSyBxlFtDwa7ahb1pA-A5pzdgnzcgFwvVlq4 -->
        ```

5.  **Create `student_data.json`:**
    *   Place the `student_data.json` file in the project root directory with your initial student data.

6.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

## API Documentation

Automatically generated documentation is available at `http://localhost:8000/docs` (Swagger UI) and `http://localhost:8000/redoc` (ReDoc).

## Endpoints

- `GET /api/v1/students/` - List students with pagination and filtering
- `POST /api/v1/students/` - Create a new student
- `GET /api/v1/students/{id}` - Get a specific student
- `PUT /api/v1/students/{id}` - Update a specific student
- `DELETE /api/v1/students/{id}` - Delete a specific student
- `GET /api/v1/search/students?q={query}` - SearchPOST /api/v1/chat/query-student-data` - Query student data using natural language (AI Chatbot)
