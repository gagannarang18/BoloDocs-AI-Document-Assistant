# 🔍 BoloDocs – Advanced RAG Document Assistant

## 📘 Overview
BoloDocs is an advanced Retrieval-Augmented Generation (RAG) system for intelligent document processing. It combines text and image understanding from PDFs using Gemini Vision and AWS Bedrock, powered by modern LLMs like LLaMA2 and LLaMA3.

Built for robust performance and seamless interaction, it supports vector-based document retrieval via AstraDB and provides a natural language interface to query document insights.

## 🚀 Features
- Text and image-based PDF analysis
- Visual content understanding with Gemini Vision
- LLM-powered reasoning via AWS Bedrock (LLaMA2 / LLaMA3)
- AstraDB vector storage for efficient RAG pipeline
- Natural language Q&A over document content

## ⚙️ Configuration
Create a `.env` file in the root directory with the following content:
```env
ASTRA_DB_TOKEN=your_token
ASTRA_DB_ENDPOINT=your_endpoint
GEMINI_API_KEY=your_key
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret


## 🖥️ Usage
```bash
streamlit run interface/streamlit_app.py
```
