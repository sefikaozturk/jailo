import streamlit as st 
import requests

st.title("Will You Go to Jail For This Tweet") 
st.markdown("Enter your tweet and select a country to get a legal risk score.")

tweet_text = st.text_area("Enter tweet text:") 
country_choice = st.selectbox("Choose Country:", options=["USA", "UK", "Germany"])

if st.button("Analyze Tweet"): 
    with st.spinner("Analyzing tweet with CrewAI..."): 
        API_URL = "https://crew-automation-agent-creation-c0fe66b5-733-15e36796.crewai.com/analyzeTweet" 
        response = requests.post(API_URL, json={"tweet_text": tweet_text, "country_choice": country_choice}) 
        crewAI_response = response.json()

        st.subheader("Risk Percentage")
        st.write(f"{crewAI_response['riskPercentage']}%")

        with st.expander("Show Detailed Report"):
            for category, details in crewAI_response["detailedReport"]["categories"].items():
                st.markdown(f"### {category}")
                st.write(f"Risk: {details['risk']}%")
                st.write(details["info"])
            st.markdown("### Overall Notes")
            st.write(crewAI_response["detailedReport"]["overallNotes"])
