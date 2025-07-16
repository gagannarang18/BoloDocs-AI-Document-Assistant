import os
import tempfile
from typing import List
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pdf2image import convert_from_path
import google.generativeai as genai

class DocumentProcessor:
    def __init__(self, gemini_api_key: str):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=10000,
            chunk_overlap=1000
        )
        genai.configure(api_key=gemini_api_key)
        self.vision_model = genai.GenerativeModel("gemini-1.5-flash")

    def _extract_image_text(self, pdf_path: str) -> str:
        images = convert_from_path(pdf_path)
        return "\n".join([
            self.vision_model.generate_content([img]).text
            for img in images
        ])

    def process_pdf(self, uploaded_file) -> List[Document]:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_path = tmp_file.name

        try:
            # Text extraction
            loader = PyPDFLoader(tmp_path)
            documents = loader.load()
            
            # Image extraction
            image_text = self._extract_image_text(tmp_path)
            
            # Combine content
            combined_text = "\n".join([doc.page_content for doc in documents]) + "\n" + image_text
            
            # Wrap combined text in a Document instance to satisfy split_documents requirements
            combined_document = Document(page_content=combined_text)
            
            return self.text_splitter.split_documents([combined_document])
        finally:
            os.unlink(tmp_path)  