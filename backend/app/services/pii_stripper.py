import io
import re
from PyPDF2 import PdfReader

class ResumeProcessor:
    @staticmethod
    def extract_text_from_pdf(pdf_bytes: bytes) -> str:
        """Extracts text from a given PDF byte stream."""
        reader = PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text

    @staticmethod
    def strip_pii(text: str) -> str:
        """Strips basic PII like email and phone numbers using regex."""
        # Regex for email
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        text = re.sub(email_pattern, '[REDACTED_EMAIL]', text)

        # Regex for phone numbers (basic international/US formats)
        phone_pattern = r'(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}'
        text = re.sub(phone_pattern, '[REDACTED_PHONE]', text)

        # Note: For production, integrate Microsoft Presidio or SpaCy here.
        return text

    @classmethod
    def process_pdf(cls, pdf_bytes: bytes) -> str:
        raw_text = cls.extract_text_from_pdf(pdf_bytes)
        sanitized_text = cls.strip_pii(raw_text)
        return sanitized_text
