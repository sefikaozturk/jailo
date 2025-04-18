import streamlit as st
from collector import CountryLegalDataCollector
from aggregator import LegalDataAggregator
from evaluator import DynamicRiskEvaluationAgent
from reporter import ReportGenerator
from crewai import Task, Crew, Process
import json

# Apply background and ensure text stays visible on top

background_image = "/Users/sefikaozturk/Downloads/tweet_legal_risk/background.png"
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url({background_image});
        background-size: cover;
        background-position: center center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

#st.set_page_config(page_title="Tweet Legal Risk Analyzer", layout="centered")
st.title("Will You Go to Jail for This Tweet?")
st.markdown("🛡️ Enter your tweet and select a country to get a legal risk score.")

# User inputs
country = st.text_input("Country (e.g., US, UK, Germany):", value="US")
tweet = st.text_area("Enter your tweet here:")

if st.button("Analyze Tweet"):
    if not tweet.strip():
        st.error("Please enter a tweet to analyze.")
    else:
        with st.spinner("Analyzing legal risk..."):
            # Task 1: Collect legal data
            collect_task = Task(
                name="collect_legal_data",
                agent=CountryLegalDataCollector(),
                description="Retrieve raw legal guidelines for the chosen country",
                params={"country": country},
                expected_output="dict mapping category names to {'text':…, 'url':…}"
            )

            # Task 2: Aggregate and structure legal data
            aggregate_task = Task(
                name="aggregate_legal_data",
                agent=LegalDataAggregator(),
                description="Structure and attach citations to the raw legal data",
                params={"legal_data": "{collect_legal_data}"},
                expected_output="dict mapping category names to {'text':…, 'citation':…}"
            )

            # Task 3: Evaluate the tweet content against legal data
            evaluate_task = Task(
                name="evaluate_tweet",
                agent=DynamicRiskEvaluationAgent(),
                description="Compute per-category and overall risk scores for the tweet",
                params={
                    "tweet": tweet,
                    "legal_data": "{aggregate_legal_data}"
                },
                expected_output="dict with 'per_category':{…}, 'overall_risk': float"
            )

            # Task 4: Generate the final report
            report_task = Task(
                name="generate_report",
                agent=ReportGenerator(),
                description="Format the evaluation into a human‑readable summary and details",
                params={"evaluation": "{evaluate_tweet}"},
                expected_output="dict with 'summary', 'details', and 'full_report' strings"
            )

            # Orchestrate the crew sequentially
            crew = Crew(
                name="TweetLegalRiskCrew",
                tasks=[collect_task, aggregate_task, evaluate_task, report_task],
                process=Process.sequential,
                verbose=False
            )

            # Run the crew
            result = crew.kickoff()

            # === Display ===

            # After kickoff():
            raw = result.raw
            try:
                output = json.loads(raw)
            except json.JSONDecodeError:
                st.error("Failed to parse crew output as JSON:")
                st.code(raw)
                st.stop()

            # Now output is a dict
            st.subheader("Overall Risk")
            st.markdown(output.get("summary", "N/A"))

            st.subheader("Category Breakdown")
            details = output.get("details", {})
            for category, info in details.items():
                with st.expander(category):
                    st.markdown(f"**Risk Score:** {info.get('risk_score', 'N/A')}%")
                    st.markdown(f"**Citation:** {info.get('citation', 'N/A')}")
                    st.write(info.get("text", ""))

            # etc…

