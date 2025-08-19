from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_together import ChatTogether, TogetherEmbeddings
import os

TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY", "KEY")
DOC_PATH = "docs"
CHROMA_PATH = "chroma_vectors"
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"

def load_documents_from_directory(directory: str = DOC_PATH) -> list[Document]:
    """
    Load all PDF and Markdown files from a directory into LangChain Document objects.
    """
    documents = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if filename.lower().endswith(".pdf"):
            loader = PyPDFLoader(filepath)
            documents.extend(loader.load())

        elif filename.lower().endswith(".md"):
            loader = TextLoader(filepath, encoding="utf-8")
            documents.extend(loader.load())

    return documents

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    split_text = text_splitter.split_documents(documents)
    return split_text

def save_vectors(documents: list[Document]):
    embedding = TogetherEmbeddings(model=EMBEDDING_MODEL, api_key=TOGETHER_API_KEY)
    Chroma.from_documents(
        documents=documents,
        embedding=embedding,
        persist_directory=CHROMA_PATH,
    )

def get_embeddings(query):
    if query:
        embedding = TogetherEmbeddings(model=EMBEDDING_MODEL, api_key=TOGETHER_API_KEY)
        vector_store = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embedding
        )
        return vector_store.similarity_search(query, k=3)
    return "No Results Found"

def format_context(docs: list[Document]) -> str:
    return "\n\n".join([doc.page_content for doc in docs])

system_message = (
    "You are a helpful assistant that ONLY answers questions based on the "
    "provided context. If no relevant context is provided, do NOT answer the "
    "question and politely inform the user that you don't have the necessary "
    "information to answer their question accurately."
)
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_message),
    HumanMessagePromptTemplate.from_template(
        "Context:\n{context}\n\nQuestion: {query}"
    )
])

llm = ChatTogether(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    api_key=TOGETHER_API_KEY,
)

if __name__ == "__main__":
    docs = load_documents_from_directory("docs")
    doc_chunks = split_documents(docs)
    save_vectors(doc_chunks)

    query1 = "How do you install unsloth for LLM fine tuning?"
    context1 = get_embeddings(query1)
    messages1 = prompt.format_messages(
        context=format_context(context1),
        query=query1
    )
    response1 = llm.invoke(messages1)
    print(response1.content)

    query2 = "What is a transformation attention layer?"
    context2 = get_embeddings(query2)
    messages2 = prompt.format_messages(
        context=format_context(context2),
        query=query2
    )
    response2 = llm.invoke(messages2)
    print(response2.content)