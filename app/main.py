import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")

    # Top branding section
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                """
                <h1 style='text-align: center; font-size: 32px; color: #1f77b4; font-weight: 700;'>
                    🚀 Imbuelucent Technologies
                </h1>
                <h2 style='text-align: center; color: #444;'>📧 Cold Mail Generator</h2>
                <p style='text-align: center; font-size: 16px; color: #666;'>
                    Automate your job outreach emails with precision and personalization.
                </p>
                """,
                unsafe_allow_html=True
            )

    # Input section
    with st.container():
        st.markdown("---")
        st.markdown("### 🔗 Provide Job Listing URL")
        url_input = st.text_input("Enter a URL:", value="https://careers.google.com/jobs/results/")
        submit_button = st.button("🚀 Generate Cold Emails")

    # Result section
    if submit_button:
        with st.spinner("Generating your cold emails..."):
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)
                st.success(f"✅ Found {len(jobs)} job(s). Generating emails...")
                for idx, job in enumerate(jobs, start=1):
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)
                    st.markdown(f"---\n### ✉️ Email for Job #{idx}")
                    st.code(email, language='markdown')
            except Exception as e:
                st.error(f"❌ An Error Occurred:\n\n{e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
