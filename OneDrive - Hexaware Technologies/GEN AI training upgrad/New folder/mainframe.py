import streamlit as st
import os
import openai
from openai import AzureOpenAI

AZURE_ENDPOINT = "https://hexavarsity-secureapi.azurewebsites.net/api/azureai"

API_KEY = "80597e18d74f981e"

API_VERSION = "2024-02-15-preview"

MODEL = "gpt-4o-mini"

openai = AzureOpenAI(

    azure_endpoint=AZURE_ENDPOINT,

    api_key=API_KEY,

    api_version=API_VERSION

)

# Function to generate documentation using OpenAI GPT
def generate_documentation(code_text, model="gpt-4o-mini", max_tokens=500):
    messages = ({"role": "system", "content": "You are an expert mainframe application documentation generator."},
                {"role": "user", "content": f"""
                 Given the following mainframe source code, generate detailed, clear \n
                 documentation explaining the purpose, main components, and functionality of the code.\n
                 Format the documentation with sections and bullet points if applicable.\n
                 "=== Source Code Start ===\n"
                 f"{code_text}\n"
                 "=== Source Code End ===\n\n"
                 "=== Documentation Start ===\n"
                 """}
    )
    try:
        # Generate the response using the chat-completions endpoint
        response = openai.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",   
        max_tokens=500,
        temperature=0.7
    )
        doc_text = response.choices[0].message.content.strip()
        return doc_text
    except Exception as e:
        return f"Error generating documentation: {e}"


def main():
    st.set_page_config(page_title="Mainframe App Automated Documentation Generator", page_icon="📄", layout="wide")
    st.title("Automated Documentation Generator for Mainframe Applications Using Generative AI")
    st.markdown(
        """
        Upload your mainframe source code files (e.g., COBOL, JCL, PL/I) below.
        This app will generate clear, comprehensive documentation using AI.
        You need to provide your OpenAI API key to generate documentation.

        #### How to use:
        1. Enter your OpenAI API key (you can get it from https://platform.openai.com/account/api-keys).
        2. Upload one or multiple source code files.
        3. Press the Generate Documentation button.
        4. View or download the generated documentation.
        """
    )

    # Input API Key

    openai.api_key = "80597e18d74f981e"

    # File uploader for multiple files
    uploaded_files = st.file_uploader("Upload Source Code Files", type=["cob","cbl","txt","jcl","pli","src"], accept_multiple_files=True)
    if uploaded_files:
        combined_code = ""
        filenames = []
        for uploaded_file in uploaded_files:
            # Read file content
            content = uploaded_file.read().decode("utf-8", errors="ignore")
            combined_code += f"\n\n// File: {uploaded_file.name}\n{content}\n"
            filenames.append(uploaded_file.name)
        st.info(f"{len(uploaded_files)} file(s) loaded for documentation generation.")
        
        #button check
        if st.button("Generate Documentation"):
            with st.spinner("Generating documentation using Generative AI..."):
                documentation = generate_documentation(combined_code)
                st.subheader("Generated Documentation")
                st.markdown(documentation)

                # Option to download documentation as text file
                st.download_button(
                    label="Download Documentation",
                    data=documentation,
                    file_name="mainframe_documentation.txt",
                    mime="text/plain"
                )

    

    
if __name__ == "__main__":
    main()

