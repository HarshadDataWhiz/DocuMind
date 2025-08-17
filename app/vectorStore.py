from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import pickle


class vectorStore:
    def split_text(pages: list):
        text_splitter = RecursiveCharacterTextSplitter(
                chunk_size = 1000,
                chunk_overlap = 250,
                add_start_index = True
            )
        all_splits = text_splitter.split_documents(pages)
        return all_splits

    def create_vector_store(all_splits: list):
        embedding = HuggingFaceEmbeddings(
            model_name = "sentence-transformers/all-mpnet-base-v2"
        )
        vector_store = InMemoryVectorStore.from_documents(
            all_splits, embedding
        )
        return vector_store

    def search(question: str, vector_store ) -> list:
        pages = vector_store.similarity_search(
            query = question,
            k = 3
        )
        pages_data = []
        for page in pages:
            dict_ = {
               # "doc_title": page.metadata['title'].strip(),
                "page_no": page.metadata['page_label'].strip(),
                "page_content": page.page_content.strip()
            }
            pages_data.append(dict_)
        return pages_data