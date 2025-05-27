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

def generate_care_plan_llm(patient_name, age, conditions, health_goals, treatment_plan, follow_up):
    # Define the messages for the chat model
    messages = [
        {"role": "system", "content": "You are a helpful healthcare assistant."},
        {"role": "user", "content": f"""
        Create a detailed and personalized care plan for the following patient:
        
        Patient Details:
        - Name: {patient_name}
        - Age: {age}
        - Medical Conditions: {', '.join(conditions)}
        
        Health Goals:
        - {', '.join(health_goals)}
        
        Treatment Plan:
        - {', '.join(treatment_plan)}
        
        Follow-Up Instructions:
        - {follow_up}
        """}
    ]

    
    
    # Generate the response using the chat-completions endpoint
    response = openai.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",  # Replace this with your deployed model name, e.g., gpt-3.5-turbo
        max_tokens=500,
        temperature=0.7
    )
    
    # Extract and return the generated text
    return response.choices[0].message.content.strip()


# Example Input
patient_name = "John Doe"
age = 45
conditions = ["Diabetes", "Hypertension"]
health_goals = ["Maintain blood sugar levels", "Reduce blood pressure", "Lose weight"]
treatment_plan = ["Take prescribed medications", "Follow a balanced diet", "Exercise for 30 minutes daily"]
follow_up = "Visit the clinic in 3 months for a progress review."

# Generate Care Plan using LLM
care_plan = generate_care_plan_llm(patient_name, age, conditions, health_goals, treatment_plan, follow_up)

# Print the Care Plan
print(care_plan)

