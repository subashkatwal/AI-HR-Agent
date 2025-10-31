import fitz

def extract_txt_from_pdf(file_path: str) -> str:
    text = ""
    with fitz.open(file_path) as doc: 
        for page in doc: 
            text += page.get_text("text")
    return text.strip()
