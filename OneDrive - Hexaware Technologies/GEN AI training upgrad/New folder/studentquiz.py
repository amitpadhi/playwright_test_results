import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

import base64

def add_background_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/jpeg;base64,{encoded_image});
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function and pass the local image filename
add_background_from_local("background.png")


# Initialize session variables for quiz and progress
if "quiz_scores" not in st.session_state:
    st.session_state.quiz_scores = []
if "quiz_attempts" not in st.session_state:
    st.session_state.quiz_attempts = []
    
# Chat-based assistance function
def ask_llm(question):
    """Query Azure OpenAI for chat-based learning assistance."""
    messages = [
        {"role": "system", "content": "You are a helpful learning assistant who explains concepts and solves problems for students."},
        {"role": "user", "content": question},
    ]
    
    try:
        
        # Generate the response using the chat-completions endpoint
        response = openai.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",   
        max_tokens=500,
        temperature=0.7
    ) 
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error: {e}"    

# Quiz function
def generate_quiz_question(topic):
    """
    Generate a quiz question with clear formatting from Azure OpenAI.
    """
    prompt = f"""
    Create a multiple-choice quiz question on the topic: {topic}.
    Ensure the output is in the following format:
    
    Question: [Your quiz question]
    A) [Option A]
    B) [Option B]
    C) [Option C]
    D) [Option D]
    Correct answer: [A, B, C, or D]
    """
    return ask_llm(prompt)   


# Track progress
def plot_progress():
    """Plot the student's quiz progress as a chart."""
    attempts = st.session_state.quiz_attempts
    scores = st.session_state.quiz_scores

    # Create the chart
    plt.figure(figsize=(10, 6))
    plt.plot(attempts, scores, marker='o', linestyle='-', color='blue')
    plt.title("Quiz Progress Over Time")
    plt.xlabel("Quiz Attempt")
    plt.ylabel("Score (%)")
    plt.ylim(0, 100)
    plt.grid()
    st.pyplot(plt)
    

# Streamlit UI
st.title("Learning Companion for Students 📚")
st.sidebar.title("Features")
feature = st.sidebar.radio("Choose a feature:", ["Chat Assistance", "Interactive Quiz", "Progress Tracker"])

if feature == "Chat Assistance":
    st.header("Chat-Based Assistance")
    user_question = st.text_area("Ask a question about a concept or problem:")
    if st.button("Get Answer"):
        if user_question.strip():
            with st.spinner("Getting your answer..."):
                response = ask_llm(user_question)
            st.markdown(f"**Answer:**\n{response}")
        else:
            st.warning("Please ask a question.")

elif feature == "Interactive Quiz":
    st.header("Interactive Quiz")

    # Topic input for the quiz
    topic = st.text_input("Enter a topic for your quiz:")

    # Generate question button
    if st.button("Generate Question"):
        if topic.strip():
            with st.spinner("Generating your quiz question..."):
                quiz = generate_quiz_question(topic)

                # Parse the quiz response to separate the question and the correct answer
                try:
                    question_text = quiz.split("Correct answer:")[0].strip()
                    correct_answer = quiz.split("Correct answer:")[-1].strip()

                    # Store in session state
                    st.session_state.generated_question = question_text
                    st.session_state.correct_answer = correct_answer
                    st.session_state.quiz_answer_submitted = False  # Reset answer submission state

                except IndexError:
                    st.error("The question format is incorrect. Please try another topic.")
        else:
            st.warning("Please enter a topic.")

    # Display question only if it exists in session state
    if "generated_question" in st.session_state:
        st.markdown(f"**Quiz Question:**\n{st.session_state.generated_question}")

        # Answer input box only appears if the user hasn't already submitted their answer
        if not st.session_state.get("quiz_answer_submitted", False):
            user_answer = st.text_input("Enter your answer (A, B, C, or D):")
            if st.button("Submit Answer"):
                # Validate the answer
                if user_answer.strip().upper() == st.session_state.correct_answer.upper():
                    st.success("Correct! Great job!")
                    score = 100
                else:
                    st.error(f"Incorrect. The correct answer was {st.session_state.correct_answer}.")
                    score = 0

                # Update session state with progress
                st.session_state.quiz_scores.append(score)
                st.session_state.quiz_attempts.append(len(st.session_state.quiz_attempts) + 1)
                st.session_state.quiz_answer_submitted = True  # Mark answer as submitted

        else:
            st.info("You have already submitted your answer for this quiz. Generate a new question to continue.")
 
elif feature == "Progress Tracker":
    st.header("Progress Tracker")
    if len(st.session_state.quiz_scores) > 0:
        st.subheader("Your Quiz Progress:")
        plot_progress()
    else:
        st.info("No quiz attempts yet. Take a quiz to track your progress!")    

# Footer
st.sidebar.info("Developed using Streamlit, Azure OpenAI, and Python.")

