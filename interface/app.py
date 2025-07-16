import streamlit as st
import sys
from pathlib import Path
# Add project root to Python path (adjust parents if needed)
sys.path.append(str(Path(__file__).resolve().parents[1]))  # Goes up 1 level to BOLODOCS
from config.settings import settings
from core.document_processor import DocumentProcessor
from core.vector_db import AstraDBManager
from core.ai_handlers import AIHandler
import sys
import os
from config.settings import settings


# Initialize core components
processor = DocumentProcessor(settings.GEMINI_API_KEY)
db_manager = AstraDBManager()
ai_handler = AIHandler()

def main():
    st.set_page_config(
        page_title="BoloDocs",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Enhanced CSS Styling
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
            
            * {
                font-family: 'Poppins', sans-serif;
            }
            
            .stApp {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            }
            
            h1 {
                text-align: center;
                background: linear-gradient(45deg, #2c3e50, #3498db);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 700;
                margin-bottom: 1.5rem;
                padding: 0.5rem;
            }
            
            .stButton>button {
                background: linear-gradient(45deg, #3498db, #2980b9);
                color: white !important;
                border: none !important;
                border-radius: 25px;
                padding: 12px 30px;
                font-size: 16px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(52,152,219,0.3);
            }
            
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(52,152,219,0.4);
            }
            
            .stFileUploader>section>div {
                border: 2px dashed #3498db !important;
                border-radius: 15px;
                background: rgba(255,255,255,0.9) !important;
                padding: 2rem !important;
            }
            
            .stTextInput>div>div>input {
                border: 2px solid #3498db !important;
                border-radius: 10px;
                padding: 12px 15px !important;
                font-size: 16px;
            }
            
            .sidebar .sidebar-content {
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                box-shadow: 5px 0 15px rgba(0,0,0,0.05);
            }
            
            .stAlert {
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            
            .footer {
                text-align: center;
                padding: 1.5rem;
                color: #6c757d;
                margin-top: 3rem;
                border-top: 1px solid #dee2e6;
            }
        </style>
    """, unsafe_allow_html=True)

    # Main Content
    st.markdown("<h1>📚 BoloDocs - Smart Document Assistant</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
            <div style='text-align: center; margin-bottom: 2rem;'>
                <p style='color: #2c3e50; font-size: 1.1rem;'>
                    Transform your documents into interactive knowledge bases with AI-powered insights
                </p>
            </div>
        """, unsafe_allow_html=True)

    # File Upload Section
    uploaded_file = st.file_uploader(
        "📤 Upload Your PDF Document", 
        type=["pdf"],
        help="Supported formats: PDF files up to 200MB"
    )

    # Question Input
    user_question = st.text_input(
        "💡 Ask a Question About Your Document",
        placeholder="Example: Can you summarize the key points of this document?",
        help="Type your question here and click 'Generate Answer'"
    )

    # Sidebar Enhancements
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; margin-bottom: 2rem;'>
                <h3 style='color: #2c3e50;'>⚙️ Knowledge Base Manager</h3>
                <p style='color: #6c757d; font-size: 0.9rem;'>
                    Manage your document repository and AI settings
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Update Knowledge Base", help="Add new documents to the AI's memory"):
            if uploaded_file:
                with st.spinner("🧠 Learning from your document..."):
                    try:
                        docs = processor.process_pdf(uploaded_file)
                        db_manager.store_documents(docs)
                        st.success(f"✅ '{uploaded_file.name}' successfully integrated!")
                    except Exception as e:
                        st.error(f"⚠️ Error: {str(e)}")
            else:
                st.warning("⚠️ Please upload a PDF file first")

    # Response Section
    if st.button("🚀 Generate Answer", type="primary", use_container_width=True):
        if user_question:
            with st.spinner("🔍 Analyzing document contents..."):
                try:
                    vectorstore = db_manager.vector_store
                    llm = ai_handler.get_llama2_llm()
                    response = ai_handler.get_response_llm(llm, vectorstore, user_question)
                    
                    st.markdown("---")
                    st.markdown("### 📝 AI Response")
                    st.markdown(f"""
                        <div style='
                            background: #ffffff;
                            padding: 1.5rem;
                            border-radius: 15px;
                            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                        '>
                            {response}
                        </div>
                    """, unsafe_allow_html=True)
                    st.success("✅ Analysis Complete!")
                    
                except Exception as e:
                    st.error(f"⚠️ Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a question first")

    # Footer
    st.markdown("""
        <div class="footer">
            <p>Powered by BoloDocs AI • v1.2.0<br>
            📧 support@bolodocs.com • 🔒 Secure Document Processing</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()