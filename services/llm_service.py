import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load variables from .env
load_dotenv()


def get_api_key():
    """Get Gemini API key from .env or Streamlit secrets."""

    # 1. Try .env
    api_key = os.getenv("GEMINI_API_KEY")

    # If SKIP_LLM is set, return a dummy key to avoid real calls
    if os.getenv("SKIP_LLM", "false").lower() == "true":
        return "DUMMY_KEY"

    if api_key:
        return api_key

    # 2. Try Streamlit secrets
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")

        if api_key:
            return api_key
    except Exception:
        pass

    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Add it to your .env file or Streamlit secrets."
    )


@st.cache_resource
def get_llm():
    """Create and cache Gemini LLM, or mock LLM if SKIP_LLM is true."""

    api_key = get_api_key()

    if os.getenv("SKIP_LLM", "false").lower() == "true":
        # Return a simple mock object with an invoke method that echoes the prompt
        class MockLLM:
            def invoke(self, prompt):
                return f"Mock response: {prompt}"
        return MockLLM()

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=api_key,
        temperature=0.2,
    )

    return llm


def clean_response(response):
    """Convert Gemini response into plain text."""

    content = response.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = []

        for item in content:
            if isinstance(item, dict):
                if "text" in item:
                    text_parts.append(item["text"])

        return "\n".join(text_parts)

    return str(content)


@st.cache_data(show_spinner=False)
def ask_llm(prompt):
    """Send prompt to LLM and return response, with optional mock handling."""

    # If skipping real LLM calls, return a mock response directly
    if os.getenv("SKIP_LLM", "false").lower() == "true":
        return f"Mock response: {prompt}"

    try:
        llm = get_llm()

        response = llm.invoke(prompt)

        return clean_response(response)

    except Exception as e:

        error_message = str(e)

        # Gemini quota/rate-limit error
        if (
            "429" in error_message
            or "RESOURCE_EXHAUSTED" in error_message
            or "quota" in error_message.lower()
        ):
            return (
                "⚠️ **Gemini API quota exceeded.**\n\n"
                "Your Gemini free-tier request limit has been reached. "
                "Please wait until the quota resets or check your "
                "Gemini API usage/billing settings."
            )

        # API key error
        if (
            "API key" in error_message
            or "API_KEY" in error_message
            or "authentication" in error_message.lower()
        ):
            return (
                "❌ **Gemini API key error.**\n\n"
                "Please check your GEMINI_API_KEY in the `.env` "
                "file or Streamlit secrets."
            )

        # Other errors
        return f"❌ **Gemini API Error:**\n\n{error_message}"