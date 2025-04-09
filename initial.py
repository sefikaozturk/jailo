import streamlit as st

# Set page title and description
st.title("CrewAI Tweet Legal Risk Analyzer") 
st.markdown("Enter your tweet and select a country to get a legal risk score based on CrewAI's automation.")

# Inputs: Tweet text and country selection
tweettext = st.textarea("Enter tweet text:") 
country_choice = st.selectbox("Choose Country:", options=["USA", "UK", "Germany"])

# When the Analyze button is pressed
if st.button("Analyze Tweet"): # Simulate the CrewAI analysis process 
    # In production, this would call your CrewAI automation code 
    crewAIresponse = { "riskPercentage": 65, "detailedReport": { "categories": { "hateSpeech": { "risk": 70, "info": "The tweet contains aggressive language that might conflict with hate speech guidelines (Source: TrustedLegalSource1)." }, "incitement": { "risk": 60, "info": "Some phrases potentially encourage negative actions, consistent with incitement criteria (Source: TrustedLegalSource2)." }, "defamation": { "risk": 55, "info": "The content could be viewed as defaming, based on legal texts for the chosen country (Source: TrustedLegalSource3)." } }, "overallNotes": f"The analysis is based on matching tweet content with current legal guidelines for {countrychoice} as updated for 2025." } }
# Display the overall risk percentage
st.subheader("Risk Percentage")
st.write(f"{crewAI_response['riskPercentage']}%")

# Provide an expandable detailed report
with st.expander("Show Detailed Report"):
    for category, details in crewAI_response["detailedReport"]["categories"].items():
        st.markdown(f"### {category}")
        st.write(f"Risk: {details['risk']}%")
        st.write(details["info"])
    st.markdown("### Overall Notes")
    st.write(crewAI_response["detailedReport"]["overallNotes"])
