from io import BytesIO
from pypdf import PdfReader
from docx import Document


def extract_text_from_file(uploaded_file):
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_pdf(uploaded_file)

    elif file_name.endswith(".docx"):
        return extract_docx(uploaded_file)

    elif file_name.endswith(".txt"):
        return extract_txt(uploaded_file)

    else:
        return None, "Unsupported file type. Please upload PDF, DOCX, or TXT."


def extract_pdf(uploaded_file):
    try:
        reader = PdfReader(BytesIO(uploaded_file.getvalue()))

        if reader.is_encrypted:
            return None, "Password-protected PDF is not supported."

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        if not text.strip():
            return None, "No text found. This may be a scanned PDF."

        return text, None

    except Exception as e:
        return None, f"PDF reading error: {e}"


def extract_docx(uploaded_file):
    try:
        document = Document(BytesIO(uploaded_file.getvalue()))

        text = ""

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                text += paragraph.text + "\n"

        if not text.strip():
            return None, "DOCX file is empty."

        return text, None

    except Exception as e:
        return None, f"DOCX reading error: {e}"


def extract_txt(uploaded_file):
    try:
        text = uploaded_file.getvalue().decode("utf-8")

        if not text.strip():
            return None, "TXT file is empty."

        return text, None

    except Exception as e:
        return None, f"TXT reading error: {e}"