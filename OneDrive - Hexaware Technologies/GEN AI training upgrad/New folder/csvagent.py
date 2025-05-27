import streamlit as st
import pandas as pd
import json
import openai
import os
import re
import matplotlib.pyplot as plt
from langchain_experimental.agents import create_csv_agent
from langchain.chat_models import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from langchain.agents.agent_types import AgentType
import os
from openai import AzureOpenAI
from dotenv import load_dotenv 


load_dotenv("/.env")

os.environ["AZURE_OPENAI_API_KEY"] = os.environ.get("AZURE_OPENAI_API_KEY")
os.environ["AZURE_OPENAI_ENDPOINT"] = os.environ.get("AZURE_OPENAI_ENDPOINT")
os.environ["AZURE_OPENAI_API_VERSION"] = os.environ.get("AZURE_OPENAI_API_VERSION")

openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
#openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = "2023-05-15-preview" 
openai.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")


csv_file_path = 'news.csv'
data = pd.read_csv(csv_file_path)
#print(data)

openai = AzureOpenAI(
    azure_endpoint=openai.azure_endpoint,
    api_key=openai.api_key ,
    api_version=openai.api_version
)

def query_openai(prompt):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

conversation = [{"role": "user", "content": "what is the capital of India" }]


#def process_csv_query(question):
    # Convert the DataFrame to a string format for querying
#    data_str = data.to_string(index=False)
    
    # Create a prompt that includes the CSV data and the user's question
#    prompt = f"Given the following CSV data:\n{data_str}\n\n" \
#             f"Please answer the following question: {question}"
    
    # Query OpenAI with the constructed prompt
#    answer = query_openai(prompt)
#    return answer


# Example question
#question = "how many rows are there?"

# Get the answer from the CSV agent
#answer = process_csv_query(question)

# Print the answer
#print("Answer:", answer)

#create CSV Files
#llm = AzureChatOpenAI(api_version=os.environ["AZURE_OPENAI_API_VERSION"])
#agent = create_csv_agent(llm, './news.csv',allow_dangerous_code=True, verbose=True)

# Example queries
#print(agent.run("How many rows of data do you have?"))


 