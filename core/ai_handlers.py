import google.generativeai as genai
from langchain_aws import BedrockEmbeddings     
from langchain_community.llms import Bedrock
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from config.settings import settings

class AIHandler:
    def __init__(self):
        # Gemini Configuration
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        # Bedrock Configuration
        self.bedrock_client = Bedrock(
            model_id="meta.llama3-70b-instruct-v1:0",
            model_kwargs={'max_gen_len': 512}
        )

    def get_gemini_vision(self):
        return genai.GenerativeModel("gemini-1.5-flash")

    def get_llama2_llm(self):
        return self.bedrock_client

    def get_response_llm(self, llm, vectorstore, query):
        """Handle the QA retrieval process"""
        prompt_template = """
        Human: Use the following context to provide a detailed answer. 
        Use at least 250-300 words with explanations if there is enough information available otherwise give the answer accordingly and precisely. If unsure, say you don't know.
        
        <context>
        {context}
        </context>
        
        Question: {question}
        
        Assistant:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        result = qa({"query": query})
        return result['result']