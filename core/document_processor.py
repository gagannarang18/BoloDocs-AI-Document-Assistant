import os
import tempfile
from typing import List
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import google.generativeai as genai
import fitz  # PyMuPDF

class DocumentProcessor:
    def __init__(self, gemini_api_key: str):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=10000,
            chunk_overlap=1000
        )
        genai.configure(api_key=gemini_api_key)
        self.vision_model = genai.GenerativeModel("gemini-1.5-flash")

    def _extract_image_text_with_fitz(self, pdf_path: str) -> str:
        doc = fitz.open(pdf_path)
        image_texts = []
        for page_num, page in enumerate(doc, start=1):
            pix = page.get_pixmap(dpi=150)  # Adjust DPI if needed
            image_bytes = pix.tobytes("png")
            try:
                response = self.vision_model.generate_content([image_bytes])
                if response.text:
                    image_texts.append(response.text)
            except Exception as e:
                image_texts.append(f"[Page {page_num}] Gemini error: {str(e)}")
        doc.close()
        return "\n".join(image_texts)

    def process_pdf(self, uploaded_file) -> List[Document]:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_path = tmp_file.name

        try:
            # Extract text using PyPDFLoader (structured content)
            loader = PyPDFLoader(tmp_path)
            documents = loader.load()

            # Extract visual content using Gemini + fitz images
            image_text = self._extract_image_text_with_fitz(tmp_path)

            # Combine both text and image-extracted text
            combined_text = "\n".join([doc.page_content for doc in documents]) + "\n" + image_text

            # Wrap and split
            combined_document = Document(page_content=combined_text)
            return self.text_splitter.split_documents([combined_document])

        finally:
            os.unlink(tmp_path)
