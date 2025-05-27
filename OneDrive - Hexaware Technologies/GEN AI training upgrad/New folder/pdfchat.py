import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text
    


# Function to respond to user queries based on extracted text
def respond_to_query(text, query):
    # Split the text into sentences for better matching
    sentences = text.split('. ')
    sentences = [s.strip() for s in sentences if s]  # Clean up sentences

    # Create a TF-IDF Vectorizer
    vectorizer = TfidfVectorizer().fit_transform(sentences + [query])
    vectors = vectorizer.toarray()

    # Calculate cosine similarity between the query and sentences
    cosine_similarities = cosine_similarity(vectors[-1:], vectors[:-1]).flatten()

    # Get the index of the most similar sentence
    most_similar_index = np.argmax(cosine_similarities)

    # Return the most similar sentence as the response
    if cosine_similarities[most_similar_index] > 0:
        return sentences[most_similar_index]
    else:
        return "Sorry, I couldn't find an answer to your question."


# Streamlit app
def main():
    st.title("PDF Chatbot")
    st.write("Upload a PDF file and ask questions about its content.")

    # File uploader for PDF
    pdf_file = st.file_uploader("Choose a PDF file", type="pdf")

    if pdf_file is not None:
        # Extract text from the uploaded PDF
        text = extract_text_from_pdf(pdf_file)
        #st.write("Text extracted from the PDF:")
        #st.write(text)

        # User input for query
        query = st.text_input("Ask a question about the PDF content:")

        if st.button("Submit"):
            if query:
                response = respond_to_query(text, query)
                st.write(response)
            else:
                st.write("Please enter a query.")

if __name__ == "__main__":
    main()
