# src/pdf_processing.py
import fitz  # PyMuPDF

def extract_text_from_pdf(path_or_fileobj):
    """
    Accepts a file path or a file-like object (werkzeug FileStorage).
    Returns concatenated text (string).
    """
    # If it's a file-like object (upload), read bytes and open with fitz
    if hasattr(path_or_fileobj, "read"):
        data = path_or_fileobj.read()
        # if the upload stream was already read earlier, rewind before calling this function
        doc = fitz.open(stream=data, filetype="pdf")
    else:
        doc = fitz.open(path_or_fileobj)

    texts = []
    for page in doc:
        try:
            txt = page.get_text("text")
        except Exception:
            txt = page.get_text()
        if txt:
            texts.append(txt)
    doc.close()
    return "\n\n".join(texts)
