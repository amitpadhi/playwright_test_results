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


def generate_performance_review(employee_name,review_period,reviewer_name,Date,
                                achievements, strengths, areas_for_improvement, goals, openai):
    """
    Generate a performance review using Azure OpenAI.
    """
    # Define messages for the chat completion request
    messages = [
        {"role": "system", "content": "You are an HR assistant who writes professional and constructive performance reviews for employees."},
        {"role": "user", "content": f"""
        Write a performance review for the following employee:

        Employee Name: {employee_name}
        
        Review Period: {review_period} 
        
        Reviewer: {reviewer_name}
        
        Date:{Date}
        

        Achievements:
        {', '.join(achievements)}

        Strengths:
        {', '.join(strengths)}

        Areas for Improvement:
        {', '.join(areas_for_improvement)}

        Future Goals:
        {', '.join(goals)}

        Provide the review in a formal yet encouraging tone.
        """}
    ]

    # Generate the response using the chat-completions endpoint
    response = openai.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",   
        max_tokens=500,
        temperature=0.7
    )
    

    # Extract and return the response content
    return response.choices[0].message.content.strip()


def process_employee_reviews(input_file, output_file, openai):
    """
    Read employee data from an Excel file, generate performance reviews, and save to a new Excel file.
    """
    # Load employee data from the input Excel file
    employee_data = pd.read_excel(input_file)
    
    employee_data.columns = employee_data.columns.str.strip()

    # Add a new column for the generated performance reviews
    employee_data['Performance Review'] = ""

    # Iterate over each employee in the Excel file
    for index, row in employee_data.iterrows():
        try:
            # Extract employee data
            employee_name = row['Name']
            achievements = row['Achievements'].split('; ')
            strengths = row['Strengths'].split('; ')
            areas_for_improvement = row['Areas for Improvement'].split('; ')
            goals = row['Goals'].split('; ')
            review_period = row['Review Period']
            reviewer_name = row['Reviewer']
            Date = row['Date']           

            # Generate performance review
            performance_review = generate_performance_review(
                employee_name, review_period ,reviewer_name ,Date,
                achievements, strengths, areas_for_improvement, goals, openai
            )

            # Add the performance review to the DataFrame
            employee_data.at[index, 'Performance Review'] = performance_review

        except Exception as e:
            print(f"Error generating review for {row['Name']}: {e}")

    # Save the updated DataFrame to a new Excel file
    employee_data.to_excel(output_file, index=False)
    print(f"Performance reviews have been saved to {output_file}")


def main():
    """
    Main function to configure the Azure OpenAI client and process the reviews.
    """
    
    # Define input and output Excel file paths
    input_file = "Employee_Data.xlsx"  # Replace with your input Excel file path
    output_file = "employee_reviews.xlsx"  # Replace with your output Excel file path

    # Process employee reviews
    process_employee_reviews(input_file, output_file,openai)



# Run the main function
if __name__ == "__main__":
    main()
 
