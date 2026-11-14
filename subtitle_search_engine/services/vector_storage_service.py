from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores.utils import filter_complex_metadata
from config.settings import AppSettings
from typing import List,Tuple
from tqdm import tqdm
import time

class Vector_Storage_Service:
    def __init__(self):
        settings = AppSettings.load_from_yaml()
        self.persist_directory=settings.ChromaDB_PERSIST_DIRECTORY
        self.openai_model=settings.OPENAI_EMBEDDING_MODEL
        self.vector_db = None

    def prepare_documents(self, subtitle_data:tuple[int, str, str]) -> None:
        langchain_docs = []

        for (subtitle_number, subtitle_name, content) in subtitle_data:
            if content:
                doc = Document(
                    page_content=content,
                    metadata = {
                        "subtitle_number" : str(subtitle_number),
                        "subtitle_name" : subtitle_name
                    }
                )
                langchain_docs.append(doc)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1800,
            chunk_overlap=400,
            separators=["\n\n", "\n", "? ", "! ", ". ", " ", ""]
        )

        self.prepared_chunks = text_splitter.split_documents(langchain_docs)

    def build_vector_store(self, api_key: str) -> None:
        embeddings = OpenAIEmbeddings(
            model= self.openai_model,
            api_key= api_key,
        )

        filtered_chunks = filter_complex_metadata(self.prepared_chunks)

        if self.load_existing_vector_store(api_key):
            print("🔄 Found existing Chroma database. Appending new files to it...")
        else:
            print("🆕 No existing database found. Creating a brand new Chroma database...")
            self.vector_db = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=embeddings,
                collection_metadata={"hnsw:space": "cosine"}
            )

        chunk_batch_size = 50
        for i in tqdm(range(0, len(filtered_chunks), chunk_batch_size)):
            batch = filtered_chunks[i : i + chunk_batch_size]
            batch_ids = [f"{doc.metadata['subtitle_name']}_{doc.metadata['subtitle_number']}_{i+j}" for j, doc in enumerate(batch)]
            
            success = False
            retries = 0
            while not success and retries < 5:
                try:
                    self.vector_db.add_documents(documents=batch,ids=batch_ids)
                    success = True
                except Exception as e:
                    if "rate_limit_exceeded" in str(e).lower():
                        retries += 1
                        # If rate limited, sleep for 30 seconds to let the OpenAI window reset
                        print(f"\n⚠️ OpenAI TPM Limit reached. Backing off for 30 seconds (Attempt {retries}/5)...")
                        time.sleep(30)
                    else:
                        # Raise any non-rate-limit unexpected error immediately
                        raise e
                        
            if not success:
                print(f"\n❌ Failed to upload batch starting at index {i} after maximum retries.")
                
            # A tiny 1-second pause between successful batches keeps the flow stable
            time.sleep(1.0)

        print("Stored data in ChromaDB...")

    def load_existing_vector_store(self, api_key: str) -> bool:
        if self.vector_db:
            return True
        
        if not api_key:
            raise ValueError("A valid OpenAI API key is required to load the embedding function.")
        
        embeddings = OpenAIEmbeddings(
            model= self.openai_model,
            api_key= api_key
        )

        self.vector_db = Chroma(
            persist_directory= self.persist_directory,
            embedding_function= embeddings
        )

        if self.vector_db:
            return True
        else:
            return False

    def get_similarity_search_results(self, api_key:str, query_subtitle: str) -> List[Tuple[Document, float]]:
        if not self.vector_db:
            self.load_existing_vector_store(api_key)

        results = self.vector_db.similarity_search_with_relevance_scores(query_subtitle, k=3)
        return results