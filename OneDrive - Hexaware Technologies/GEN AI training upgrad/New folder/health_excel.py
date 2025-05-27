import openai
import pandas as pd
 
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

def generate_care_plan_llm(open_ai,patient_name, age, conditions, health_goals, treatment_plan, follow_up):
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
        model="gpt-4o-mini",   
        max_tokens=500,
        temperature=0.7
    )
    
    # Extract and return the generated text
    return response.choices[0].message.content.strip()


# Function to process Excel and generate care plans
def process_excel_and_generate_care_plans(input_excel, output_excel, openai):
    # Load the patient data from Excel
    patient_data = pd.read_excel(input_excel)
    
    patient_data.columns = patient_data.columns.str.strip()
    
    # Create a new column for the generated care plans
    care_plans = []

    # Loop through each patient in the file
    for index, row in patient_data.iterrows():
        patient_name = row['Name']
        age = row['Age']
        conditions = row['Conditions'].split(', ')
        health_goals = row['Health Goals'].split(', ')
        treatment_plan = row['Treatment Plan'].split(', ')
        follow_up = row['Follow-Up']

        # Generate care plan using Azure OpenAI
        care_plan = generate_care_plan_llm(
            openai, patient_name, age, conditions, health_goals, treatment_plan, follow_up
        )
        care_plans.append(care_plan)

    # Add the generated care plans to the DataFrame
    patient_data['Care Plan'] = care_plans

    # Save the results to a new Excel file
    patient_data.to_excel(output_excel, index=False)
    print(f"Care plans saved to {output_excel}")
    

def main():
    # Input and output Excel file paths
    input_excel = "patient.xlsx"  # Input Excel file containing patient data
    output_excel = "patients_with_care_plans.xlsx"  # Output Excel file with care plans
    openai = AzureOpenAI(

    azure_endpoint=AZURE_ENDPOINT,

    api_key=API_KEY,

    api_version=API_VERSION

)
    # Process the Excel file and generate care plans
    process_excel_and_generate_care_plans(input_excel, output_excel, openai)


    

 
# Run the main function
if __name__ == "__main__":
    main()
 
