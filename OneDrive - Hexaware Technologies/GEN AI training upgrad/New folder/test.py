# Import the libraries

import os, json, ast

import openai
 
from openai import AzureOpenAI

AZURE_ENDPOINT = "https://hexavarsity-secureapi.azurewebsites.net/api/azureai"

API_KEY = "80597e18d74f981e"

API_VERSION = "2024-02-15-preview"

MODEL = "gpt-4o-mini"

# Initialize OpenAI client

openai = AzureOpenAI(

    azure_endpoint=AZURE_ENDPOINT,

    api_key=API_KEY,

    api_version=API_VERSION

)
 
def get_chat_model_completions(messages):

    response = openai.chat.completions.create(

        model=MODEL,

        messages=messages,    

    )

    return response.choices[0]
 
conversation = [{"role": "user", "content": "what is the capital of India" }]

 
 