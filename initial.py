import streamlit as st 
import requests

st.title("Will You Go to Jail For This Tweet") 
st.markdown("Enter your tweet and select a country to get a legal risk score.")

tweet_text = st.text_area("Enter tweet text:") 
country_choice = st.selectbox("Choose Country:", options=["USA", "UK", "China", "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", 
                                                          "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", 
                                                          "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", 
                                                          "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", 
                                                          "Chad", "Chile", "China", "Colombia", "Comoros", "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba", "Cyprus", 
                                                          "Czech Republic (Czechia)", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", 
                                                          "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini (fmr. "Swaziland")", "Ethiopia", "Fiji", "Finland", "France", 
                                                          "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", 
                                                          "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan"
])

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
