import os
import pickle
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")

# Check for required environment variables
required_env_vars = [
    "AZURE_OPENAI_API_KEY",
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_API_VERSION"
]


# Create a vector database
def create_vector_database(txt_path):
    loader = TextLoader(txt_path)
    docs = loader.load()
    
    documents = RecursiveCharacterTextSplitter(
        chunk_size=1000, separators=["\n", "\n\n"], chunk_overlap=200
    ).split_documents(docs)

    embeddings = AzureOpenAIEmbeddings(
                     openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                     azure_endpoint =os.getenv("AZURE_OPENAI_ENDPOINT"),
                     model="text-embedding-ada-002" 
                        )       
    
    db = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )
    
    # Save the vector store to a pickle file
    with open("vectorstore.pkl", "wb") as f:
        pickle.dump(db, f)

    print("Vector store saved to vectorstore.pkl")

if __name__ == "__main__":
    create_vector_database("output.txt")

# Load libraries in main.py
os.environ["AZURE_OPENAI_API_KEY"] = os.environ.get("AZURE_OPENAI_API_KEY")
os.environ["AZURE_OPENAI_ENDPOINT"] = os.environ.get("AZURE_OPENAI_ENDPOINT")
os.environ["AZURE_OPENAI_API_VERSION"] = os.environ.get("AZURE_OPENAI_API_VERSION")
os.environ["AZURE_DEPLOYMENT_EMBEDDINGS"] = os.environ.get("AZURE_DEPLOYMENT_EMBEDDINGS")

# Load vector database from pickle
def load_vectorstore():
    with open("vectorstore.pkl", "rb") as f:
        vectorstore = pickle.load(f)
    return vectorstore

# Load the vector store
vectorstore_faiss = load_vectorstore()

# Configure your Chatbot Model
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    verbose=False,
    temperature=0.3,
)

# Create a Prompt for your bot
PROMPT_TEMPLATE = """You are an AI Assistant. Given the following context:
{context}

Answer the following question:
{question}

Assistant:"""

PROMPT = PromptTemplate(
    template=PROMPT_TEMPLATE, input_variables=["context", "question"]
)

# Setup your Retriever
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore_faiss.as_retriever(
        search_type="similarity", search_kwargs={"k": 6}
    ),
    verbose=False,
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT},
)

# Invoke your model
question = "What is the main topic of the document?"  # Enter your question here
response = qa.invoke({"query": question})
result = response["result"]

print("Response:", result)