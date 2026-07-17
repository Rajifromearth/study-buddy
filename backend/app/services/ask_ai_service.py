import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def ask_general(question: str, course: str | None = None) -> dict:
    """Answer an academic question using the model's general knowledge."""
    course_context = f" in the context of {course}" if course else ""
    prompt = f'''You are a helpful study assistant. Give clear, accurate, and reasonably concise educational answers. Format every response in Markdown with clear paragraphs and bullet points where appropriate. For mathematical expressions, use LaTeX wrapped in $ for inline math or $$ for display math.
Answer the following question{course_context}.

Question: {question}'''

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "answer": "The AI assistant service is not configured yet.",
        }

    try:
        response = OpenAI(api_key=api_key).responses.create(
            model="gpt-5.6-terra", input=prompt
        )
        return {"answer": response.output_text}
    except Exception as exc:
        print(f"AI assistant service error: {exc}")
        return {
            "answer": "Unable to answer the question right now due to an AI service error.",
        }