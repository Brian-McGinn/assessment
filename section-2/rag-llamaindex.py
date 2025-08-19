# llama-index
# langchain
# langchain_chroma
# langchain_community
# llama-index-embeddings-ollama
# llama-index-llms-ollama
# llama-index-vector-stores-chroma

DOC_PATH="docs"
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, PromptTemplate
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

def load_documents_from_directory(directory: str):
    """
    Load PDF and Markdown files from a directory into LlamaIndex Documents.
    """
    return SimpleDirectoryReader(input_dir=directory, required_exts=[".pdf", ".md"]).load_data()

def build_rag_system(doc_dir: str, persist_dir: str = "./chroma_store"):
    # 1. Load documents
    documents = load_documents_from_directory(doc_dir)

    # 2. Setup embedding model
    embed_model = OllamaEmbedding(model_name="nomic-embed-text", request_timeout=120)

    # 3. Setup persistent Chroma DB
    chroma_client = chromadb.PersistentClient(path=persist_dir)
    chroma_collection = chroma_client.get_or_create_collection("rag_collection")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 4. Build index
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model
    )

    return index

def load_existing_rag(persist_dir: str = "./chroma_store"):
    """
    Load an existing persistent Chroma store into LlamaIndex without re-embedding.
    """
    # 1. Setup persistent Chroma client
    chroma_client = chromadb.PersistentClient(path=persist_dir)

    # 2. Reconnect to the same collection
    chroma_collection = chroma_client.get_or_create_collection("rag_collection")

    # 3. Wrap in LlamaIndex vector store
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 4. Recreate embedding model (Ollama nomic-embed-text)
    embed_model = OllamaEmbedding(model_name="nomic-embed-text", request_timeout=120)

    # 5. Create index from existing embeddings (no re-embedding)
    index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context, embed_model=embed_model)

    return index

def query_rag(query: str):
    index = load_existing_rag()
    # Setup Ollama Llama3.1 model
    llm = Ollama(model="llama3.1", request_timeout=120)

    # Define prompt
    qa_template = PromptTemplate(
        "Use the context below to answer the question.\n\n"
        "Context:\n{context_str}\n\n"
        "Question: {query_str}\n\n"
        "Answer:"
    )

    # Create query engine with custom prompt
    query_engine = index.as_query_engine(llm=llm, text_qa_template=qa_template)

    # Run query
    response = query_engine.query(query)
    return response

if __name__ == "__main__":
    print("")
    build_rag_system("./docs")
    user_input = input("How can I help?").lower()
    result = query_rag(user_input)
    print(result)