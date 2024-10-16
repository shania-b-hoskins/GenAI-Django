# test_api.py
import os
import logging
from langchain_google_genai import ChatGoogleGenerativeAI

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set your API Key from environment variable
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Check if the API Key is retrieved correctly
if GOOGLE_API_KEY is None:
    logger.error("API key not found in environment variables.")
    exit(1)

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    api_key=GOOGLE_API_KEY,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    handle_parsing_errors=True,
    temperature=0.6,
)

# Define a test prompt
prompt = "Provide a brief investment analysis for the Technology sector."

try:
    response = llm.invoke(prompt)
    # Directly access the response content
    print("Chatbot Response:", response.content if hasattr(response, 'content') else 'No content returned.')
except Exception as e:
    logger.error(f"Error invoking chatbot: {e}")
