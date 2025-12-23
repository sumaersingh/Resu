import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Resu", layout="wide")

st.title("🤖 Resu")
st.write("Paste your resume and a job description to get ATS-style feedback.")

# Inputs
resume_text = st.text_area("📄 Paste your Resume", height=250)
job_description = st.text_area("💼 Paste the Job Description", height=250)

analyze = st.button("Analyze Resume")

if analyze:
    if resume_text.strip() == "" or job_description.strip() == "":
        st.warning("Please paste both your resume and the job description.")
    else:
        with st.spinner("Analyzing..."):
            prompt = f"""
You are an ATS resume evaluator.

Compare the RESUME to the JOB DESCRIPTION.

Return:
1. A match score out of 100
2. 5 strengths
3. 5 gaps or weaknesses
4. Missing keywords
5. 5 specific improvement suggestions

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional technical recruiter."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )

            st.subheader("📊 Analysis Results")
            st.write(response.choices[0].message.content)