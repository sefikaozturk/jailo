import streamlit as st
from crewai import Crew # Adjust this if your import is different

# Step 1: Initialize the Crew (only once)
@st.cache_resource
def load_crew():
    # Replace this with your actual Crew setup
    crew = Crew(
        agents=[...],  # your agents here
        tasks=[...],   # your tasks here
        verbose=True
    )
    return crew

# Step 2: Run CrewAI agent based on user input
def run_crew_agent(user_input: str) -> str:
    crew = load_crew()
    response = crew.run(user_input)
    
    # Optional: handle response if it's structured
    if isinstance(response, dict):
        output = ""
        for key, value in response.items():
            output += f"**{key.capitalize()}**\n{value}\n\n"
        return output
    return response

# Step 3: Streamlit UI
st.set_page_config(page_title="How Far Does $100 Go?", layout="centered")
st.title("How Far Does $100 Go?")
st.markdown("Explore purchasing power across the world and learn cultural insights from AI agents.")

# User input section
amount = st.slider("Amount of Money ($)", min_value=10, max_value=1000, step=10, value=100)
city = st.text_input("Enter a city or country", value="Manila")
category = st.selectbox("Choose a category", ["All", "Food", "Rent", "Transport", "Entertainment", "Utilities"])
question = st.text_area("Ask the AI a specific question (optional)", placeholder="e.g., Why is food cheaper in Manila than in NYC?")

# Combine input into prompt
if st.button("Run Agent"):
    with st.spinner("Analyzing..."):
        input_text = f"You have ${amount} in {city}. Category: {category}. {question}"
        result = run_crew_agent(input_text)
    st.success("Done!")
    st.markdown("### Agent Response")
    st.markdown(result)
