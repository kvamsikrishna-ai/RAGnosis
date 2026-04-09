from pypdf import PdfReader
import os

def load_pdfs(folder_path):
    documents = []

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            path = os.path.join(folder_path, file)
            reader = PdfReader(path)

            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + " "

            documents.append({
                "file_name": file,
                "content": text
            })

    return documents