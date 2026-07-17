import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def expand_explanation(
    topic: str, existing_content: str, course: str | None = None
) -> dict:
    """Expand existing academic content with a more in-depth explanation."""
    course_context = f" in the context of {course}" if course else ""
    prompt = f'''You are a helpful study assistant. Provide a significantly more detailed, in-depth explanation of the given topic{course_context}.
Build on the existing content as context instead of simply repeating it. Clarify underlying concepts, add useful examples, and explain important connections where helpful.

Format every response in Markdown with clear structure, headings or subheadings where appropriate, bullet points, and examples. For mathematical expressions, use LaTeX wrapped in $ for inline math or $$ for display math.

Topic: {topic}

Existing content:
{existing_content}'''

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "detailed_explanation": "The Learn More service is not configured yet.",
        }

    try:
        response = OpenAI(api_key=api_key).responses.create(
            model="gpt-5.6-terra", input=prompt
        )
        return {"detailed_explanation": response.output_text}
    except Exception as exc:
        print(f"Learn More service error: {exc}")
        return {
            "detailed_explanation": "Unable to expand this explanation right now due to an AI service error.",
        }