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
import base64
from dotenv import load_dotenv
import pickle

def get_base64_image(image_file):
    with open(image_file, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Load your local image
image_path = "PDF background.png"  # Change this to your local image path
background_image = get_base64_image(image_path)

# Custom CSS for background

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #f0f2f5;
        background-image: url(data:image/jpeg;base64,{background_image});
        background-size: cover;
        background-position: center;
        height: 100vh;  /* Full height */
    }}
    </style>
    """,
    unsafe_allow_html=True
)

#Load the environment and assign the corresponding values to the variables
load_dotenv("/.env")

os.environ["AZURE_OPENAI_API_KEY"] = os.environ.get("AZURE_OPENAI_API_KEY")
os.environ["AZURE_OPENAI_ENDPOINT"] = os.environ.get("AZURE_OPENAI_ENDPOINT")
os.environ["AZURE_OPENAI_API_VERSION"] = os.environ.get("AZURE_OPENAI_API_VERSION")

#sidebar contents
with st.sidebar:
    st.title('Query your Pdf files')
    st.markdown(''' 
                This app is an LLM-Powered chatbot using 
                Streamlit , Langchain and Azure OpenAI''')
    add_vertical_space(5)
    st.write("Made for PDF query results")
    

#Main processing

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

        #breaking down text into smaller, coherent chunks
        
        text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
                        chunk_size=1000,
                        chunk_overlap=200,
                        length_function=len
                        )
        chunks = text_splitter.split_text(text=text)

        # Generate embeddings for documents
        embeddings = AzureOpenAIEmbeddings(
                     openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                     azure_endpoint =os.getenv("AZURE_OPENAI_ENDPOINT"),
                     model="text-embedding-ada-002"      
                     )
        
        # stores the FAISS vector database in a directory structure, 
        # preserving metadata and index files.
        local_path = 'Local'
        vector_store = FAISS.from_texts(chunks, embeddings)
        vector_store.save_local(local_path)
        vector_store = FAISS.load_local(local_path, embeddings, allow_dangerous_deserialization=True)
        retriever = vector_store.as_retriever()
        st.write('Embeddings loaded from disk')
        
        #Add one text box for user to ask query
        query = st.text_input("Ask a question about your PDF file")
        #st.write(query)
        
        #Implement the search functionality and display the results
        if query:
            docs = vector_store.similarity_search(query=query, top_k=3)
        
            llm = AzureChatOpenAI(model_name="gpt-4o-mini",api_version="2024-02-15-preview")
            chain = load_qa_chain(llm=llm,chain_type="stuff")
            response= chain.run(input_documents=docs, question=query)
            st.write(response)
        

#Invoke the main function       
if __name__ == "__main__":
    main()          
        
        
            