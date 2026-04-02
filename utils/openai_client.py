# utils/openai_client.py
import openai
from config import settings
from typing import List, Dict, Any
import json_storage # Import our JSON utility

openai.api_key = settings.AIzaSyBxlFtDwa7ahb1pA-A5pzdgnzcgFwvVlq4
def query_student_data_natural_language(query: str) -> str:
    """
    Processes a natural language query using OpenAI and returns results from the JSON file.
    """
    system_prompt = f"""
    You are an assistant that helps query a JSON file containing student records.
    The records have the following fields:
    id (integer), first_name (string), last_name (string), email (string), enrollment_date (ISO string),
    gpa (float), major (string), year_level (integer), status (string), address (string), phone_number (string).

    When the user asks a question, translate their natural language into a specific request for student data.
    Examples:
    - User: "Show me students in Computer Science."
      Response: "Get students where major is 'Computer Science'."
    - User: "Who has a GPA above 3.5?"
      Response: "Get students where gpa > 3.5."
    - User: "Find Bola Abdullahi"
      Response: "Get the student where first_name is 'Bola' and last_name is 'Abdullahi'."
    Respond only with the translated request in plain English, focusing on the filters needed.
    """

    try:
        response = openai.ChatCompletion.create(
            model=settings.OPENAI_MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            max_tokens=150,
            temperature=0.1
        )

        ai_response = response.choices[0].message['content'].strip()
        print(f"AI Interpretation: {ai_response}") # Log for debugging

        # --- Simulate Parsing and Querying JSON ---
        # In a real implementation, you'd need robust parsing of 'ai_response'.
        # For this example, we'll just return the AI's interpretation and a fixed result based on common queries.
        # This is a significant simplification compared to database queries.

        # This is a very basic simulation of how you might filter the JSON data based on the AI's interpretation.
        # A full implementation would require much more sophisticated parsing.
        all_students = json_storage.load_students_from_file()

        # Example hardcoded filters based on AI response keywords (NOT ROBUST)
        results = []
        if "computer science" in ai_response.lower():
            results = [s for s in all_students if s.get('major', '').lower() == 'computer science']
        elif "above 3.5" in ai_response.lower() or "gpa > 3.5" in ai_response.lower():
             try:
                 results = [s for s in all_students if s.get('gpa', 0) > 3.5]
             except TypeError:
                 pass # Handle cases where gpa is not a number
        elif "Bola Abdullahi" in ai_response.lower():
             results = [s for s in all_students if s.get('first_name', '').lower() == 'john' and s.get('last_name', '').lower() == 'smith']
        else:
            # If no specific filter is recognized, return all students or a generic message
            results = all_students

        # Format results for output
        if results:
            formatted_results = "\n".join([f"- {s['first_name']} {s['last_name']} (ID: {s['id']}, Major: {s['major']}, GPA: {s.get('gpa', 'N/A')})" for s in results[:5]]) # Limit output for readability
            return f"Interpreted Query: {ai_response}\n\nFound {len(results)} matching student(s):\n{formatted_results}"
        else:
            return f"Interpreted Query: {ai_response}\n\nNo students matched the criteria."


    except Exception as e:
        print(f"Error querying OpenAI: {e}")
        return f"Error processing AI query: {str(e)}"