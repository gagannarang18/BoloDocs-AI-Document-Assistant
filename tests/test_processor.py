import pytest
from core.document_processor import DocumentProcessor
from config.settings import settings

@pytest.fixture
def document_processor():
    return DocumentProcessor(settings.GEMINI_API_KEY)

def test_pdf_processing(document_processor):
    # Add actual test implementation
    pass