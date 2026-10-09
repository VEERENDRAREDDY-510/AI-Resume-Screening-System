import os

from pypdf import PdfReader
import fitz
import pytesseract
from PIL import Image


# Tesseract executable location on Windows
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def extract_text(pdf_path):
    """
    Extract text from a PDF.

    First tries normal PDF text extraction using pypdf.
    If no text is found, uses OCR with Tesseract.
    """

    # ---------------------------------------------------------
    # STEP 1: Try normal PDF text extraction
    # ---------------------------------------------------------
    try:
        reader = PdfReader(pdf_path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        # If text was successfully extracted, return it
        if text.strip():
            return text.strip()

    except Exception as e:
        print("Normal PDF extraction failed:", e)

    # ---------------------------------------------------------
    # STEP 2: OCR scanned/image-based PDF
    # ---------------------------------------------------------
    try:
        document = fitz.open(pdf_path)

        ocr_text = ""

        for page in document:

            # Render PDF page as an image
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

            # Convert image to PIL format
            image = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            # Perform OCR
            page_text = pytesseract.image_to_string(image)

            if page_text:
                ocr_text += page_text + "\n"

        document.close()

        return ocr_text.strip()

    except Exception as e:
        print("OCR extraction failed:", e)
        return ""