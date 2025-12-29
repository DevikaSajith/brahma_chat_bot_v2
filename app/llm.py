import os
from dotenv import load_dotenv
from google import genai

# Load .env BEFORE reading variables
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise RuntimeError("❌ GOOGLE_API_KEY not found in environment")

client = genai.Client(api_key=API_KEY)
# ⚡ LIGHTWEIGHT: Use Gemma model - better rate limits than Gemini
# Available options: gemma-2-9b-it (smaller/faster), gemma-2-27b-it (larger/better)
model = "models/gemma-3-12b-it"  # or "models/gemma-2-27b-it" for better quality


def generate_answer(context: str, question: str) -> str:
    """
    Generate answer with minimal token usage, strictly using provided context.
    """
    # Truncate context if too long
    max_context_length = 1500  # characters
    if len(context) > max_context_length:
        context = context[:max_context_length] + "..."
    
    # Improved prompt with strict instructions
    prompt = f"""You are a helpful assistant for Brahma '26 cultural festival at ASIET college.

STRICT RULES:
1. Answer ONLY based on the context provided below
2. If the answer is not in the context, say "I don't have that information in my knowledge base"
3. Do NOT use external knowledge or make assumptions
4. Keep answers concise and relevant
5. Stay focused on Brahma '26 and ASIET events

Context Information:
{context}

Question: {question}

Answer (based only on the context above):"""

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config={
                'max_output_tokens': 200,  # Limit response length
                'temperature': 0.3,  # Lower temperature for more focused responses
            }
        )
        return response.text
    except Exception as e:
        print(f"❌ LLM error: {e}")
        import traceback
        traceback.print_exc()
        return "Sorry, I couldn't generate a response at this time."
