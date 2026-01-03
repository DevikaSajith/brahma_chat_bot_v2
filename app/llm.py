import os
from dotenv import load_dotenv
from google import genai

# Load .env BEFORE reading variables
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise RuntimeError("❌ GOOGLE_API_KEY not found in environment")

client = genai.Client(api_key=API_KEY)
# ⚡ OPTIMIZED FOR SPEED: Using smallest Gemma model for fastest response
model = "models/gemma-3-1b-it"  # Fastest model with good quality


def generate_answer(context: str, question: str) -> str:
    """
    Generate answer with minimal token usage, optimized for speed.
    """
    # Truncate context aggressively for faster processing
    max_context_length = 1000  # Reduced from 1500
    if len(context) > max_context_length:
        context = context[:max_context_length] + "..."
    
    # Strict prompt to prevent hallucination
    prompt = f"""You are an assistant for Brahma '26 and Ashwamedha '26 festivals at ASIET.

CRITICAL RULES:
1. ONLY use information from the context below
2. If the answer is NOT in the context, say "I don't have that information"
3. DO NOT make up or guess any information
4. DO NOT add details not present in the context
5. Keep answers brief and factual

Context:
{context}

Question: {question}

Answer (only from context above):"""

    try:
        print("🔄 Sending request to LLM...")
        print(f"context: {context}, question: {question}")
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config={
                'max_output_tokens': 150,  # Reduced for faster response
                'temperature': 0.2,  # Lower temperature to reduce creativity/hallucination
            }
        )
        return response.text
    except Exception as e:
        print(f"❌ LLM error: {e}")
        return "Sorry, I couldn't generate a response at this time."
