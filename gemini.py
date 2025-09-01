import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 500,
}

ADMIN_CONTEXT = """
You are the admin of a Telegram bot that helps Instagram accounts grow their following.
The bot pays 5 euros per account. Always respond in English, humanized and professional.
Do not reply to messages about scams or abusive language; ignore them.
Be friendly, helpful, and guide users clearly.
"""

def get_gemini_response(user_text: str) -> str:
    """
    Sends user input to Gemini AI with admin context and returns the generated response.
    """
    try:
        prompt = f"{ADMIN_CONTEXT}\n\nUser: {user_text}\nAdmin:"
        response = genai.generate_text(
            model="gemini-1.5-pro",
            prompt=prompt,
            **generation_config
        )
        if hasattr(response, "candidates") and response.candidates:
            return response.candidates[0].output_text.strip()
        return str(response)
    except Exception as e:
        return f"Error generating response: {str(e)}"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 500,
}

def get_gemini_response(user_text: str) -> str:
    """
    Sends user input to Gemini AI and returns the generated response.
    """
    try:
        response = genai.generate_text(
            model="gemini-1.5-pro",
            prompt=user_text,
            **generation_config
        )
        
        if hasattr(response, "candidates") and response.candidates:
            return response.candidates[0].output_text
        return str(response)
    except Exception as e:
        return f"Error generating response: {str(e)}"
