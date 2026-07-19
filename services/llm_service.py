import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_api_key():
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return api_key

    try:
        import streamlit as st
        api_key = st.secrets.get("GEMINI_API_KEY")

        if api_key:
            return api_key

    except Exception:
        pass

    raise ValueError("GEMINI_API_KEY not found. Add it in .env file.")


def get_llm():
    api_key = get_api_key()

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=api_key,
        temperature=0.2
    )

    return llm


def clean_response(response):
    content = response.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = []

        for item in content:
            if isinstance(item, dict) and "text" in item:
                text_parts.append(item["text"])

        return "\n".join(text_parts)

    return str(content)


def ask_llm(prompt):
    llm = get_llm()
    response = llm.invoke(prompt)
    return clean_response(response)