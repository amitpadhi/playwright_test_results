#start
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai import AzureOpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import AzureOpenAI 
from langchain_openai import AzureChatOpenAI
import os 
from dotenv import load_dotenv
import pickle

load_dotenv("/.env")

os.environ["AZURE_OPENAI_API_KEY"] = os.environ.get("AZURE_OPENAI_API_KEY")
os.environ["AZURE_OPENAI_ENDPOINT"] = os.environ.get("AZURE_OPENAI_ENDPOINT")
os.environ["AZURE_OPENAI_API_VERSION"] = os.environ.get("AZURE_OPENAI_API_VERSION")


#sidebar contents
with st.sidebar:
    st.title('LLM chat app')
    st.markdown('''    ''')
    add_vertical_space(5)
    st.write("made for sample project")
    
    
def main():
    st.header("Chat with PDF ")
    #st.write("Hello")    
    pdf=st.file_uploader("upload your PDF", type='pdf')
    #Pdf_Reader =  PdfReader(pdf)
    #st.write(Pdf_Reader)
    if pdf is not None:
        Pdf_Reader = PdfReader(pdf)
        
        text = ''
        for page in Pdf_Reader.pages:
            text += page.extract_text()   
        #st.write(text) 
        text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
                        chunk_size=1000,
                        chunk_overlap=200,
                        length_function=len
                        )
        chunks = text_splitter.split_text(text=text)
        
        embeddings = AzureOpenAIEmbeddings(
                     openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                     azure_endpoint =os.getenv("AZURE_OPENAI_ENDPOINT"),
                     model="text-embedding-ada-002"      
                     )
        vector_store = FAISS.from_texts(chunks, embeddings)
        st.write('Embeddings loaded from disk')
        
        
        query = st.text_input("Ask a question about your PDF file")
        st.write(query)
        
        docs = vector_store.similarity_search(query=query, top_k=3)
        
        llm = AzureChatOpenAI(model_name="gpt-4o-mini",api_version="2024-02-15-preview")
        chain = load_qa_chain(llm=llm,chain_type="stuff")
        response= chain.run(input_documents=docs, question=query)
        st.write(response)
        
        #st.write(chunks)
        #embeddings = OpenAIEmbeddings()
        # Create embeddings
        
        # Create a vector store
        #vector_store = FAISS.from_texts(chunks, embeddings)
        #store_name = pdf.name[:-4]
        
        #if os.path.exists(f"{store_name}.pkl"):
        #    with open(f"{store_name}.pkl", "rb") as f:
        #        vector_store = pickle.load(f)
        #        #pickle.dump(vector_store,f)
        #    st.write('Embeddings loaded from disk')
        #else:
        #    embeddings = AzureOpenAIEmbeddings(
        #             openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        #             azure_endpoint =os.getenv("AZURE_OPENAI_ENDPOINT"),
        #             model="text-embedding-ada-002"      
        #             )
        #    vector_store = FAISS.from_texts(chunks, embeddings)
        #    #vectorstore = CustomVectorStore(data)
        #    with open(f"{store_name}.pkl", "wb") as f:
        #        pickle.dump(vector_store,f) 
        #        #pickle.dump(vector_store.to_serializable(), f)
                   
        
if __name__ == "__main__":
    main()  