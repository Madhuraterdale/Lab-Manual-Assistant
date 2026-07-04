from modules.pdf_processor import PDFProcessor

pdf = PDFProcessor("uploads/sample.pdf")

text = pdf.extract_text()

print(text)