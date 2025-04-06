# BoloDocs - AI Document Assistant


## 📖 Overview
AI-powered document processing system with multi-modal PDF analysis (text + images) using Gemini AI and AWS Bedrock.

## 🚀 Features
- PDF text extraction
- Image content analysis (Gemini Vision)
- AWS Bedrock integration (Llama2/Llama3)
- AstraDB vector storage
- Natural language query interface

## ⚙️ Configuration
Create `.env` file:
```env
ASTRA_DB_TOKEN=your_token
ASTRA_DB_ENDPOINT=your_endpoint
GEMINI_API_KEY=your_key
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
```

## 🖥️ Usage
```bash
streamlit run interface/streamlit_app.py
```