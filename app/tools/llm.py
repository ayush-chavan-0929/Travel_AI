import os
import json
from dotenv import load_dotenv

load_dotenv()

_llm_instance = None

def get_gemini_llm(model_name: str = "gemini-1.5-flash", temperature: float = 0.2):
    """
    Returns an initialized ChatGoogleGenerativeAI instance if GEMINI_API_KEY / GOOGLE_API_KEY
    is set, otherwise returns None.
    Gemini API has a free tier provided by Google AI Studio.
    """
    global _llm_instance
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None
        
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=temperature
        )
        return llm
    except Exception as e:
        print(f"Warning: Could not initialize Gemini LLM: {e}")
        return None
