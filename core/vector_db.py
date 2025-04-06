from langchain_astradb.vectorstores import AstraDBVectorStore
from langchain_aws import BedrockEmbeddings     
from langchain_community.llms import Bedrock
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class AstraDBManager:
    def __init__(self):
        try:
            self.embeddings = BedrockEmbeddings(
                model_id="amazon.titan-embed-text-v2:0"
            )
            self.vector_store = AstraDBVectorStore(
                collection_name="db_minor_embeddings_v1",
                embedding=self.embeddings,
                token=settings.ASTRA_DB_APPLICATION_TOKEN,
                api_endpoint=settings.ASTRA_DB_API_ENDPOINT
            )
            logger.info("Successfully connected to AstraDB Vector Store")
        except Exception as e:
            logger.error(f"Failed to initialize AstraDB connection: {str(e)}")
            raise

    def store_documents(self, docs):
        try:
            result = self.vector_store.add_documents(docs)
            logger.info(f"Stored {len(docs)} documents successfully")
            return result  # Returns list of document IDs
        except Exception as e:
            logger.error(f"Document storage failed: {str(e)}")
            raise