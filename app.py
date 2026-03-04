import streamlit as st
import os
import time
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path

from utils.text_handler import extract_text_from_txt
from utils.pdf_handler import extract_text_from_pdf

# ===============================
# LOAD ENV
# ===============================
load_dotenv(dotenv_path=Path(".env"))

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY not found in .env file")
    st.stop()

client = OpenAI(api_key=api_key)

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="AI Research & Finance Analyzer",
    page_icon="🚀",
    layout="wide"
)

# ===============================
# CUSTOM CSS
# ===============================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

.hero-title {
    font-size: 44px;
    font-weight: 700;
    line-height: 1.2;
}

.hero-subtitle {
    font-size: 18px;
    color: #94A3B8;
    margin-top: 20px;
    line-height: 1.6;
}

.stButton > button {
    background-color: #6366F1;
    color: white;
    border-radius: 10px;
    padding: 10px 24px;
    border: none;
}

.card {
    background-color: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 15px;
    margin-top: 30px;
}

.summary-box {
    background-color: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)


# ===============================
# HERO SECTION 
# ===============================

col1, col2 = st.columns([1.2, 1])  # Text sedikit lebih besar dari image

with col1:
    st.markdown("""
        <div class="hero-title">
            AI-Powered Financial & Document Intelligence
        </div>
        <div class="hero-subtitle">
            Transform documents and financial data into actionable insights 
            using advanced AI models built for modern businesses.
        </div>
    """, unsafe_allow_html=True)

with col2:
    image_path = "assets/hero.png"
    if os.path.exists(image_path):
        st.image(image_path, width=350)  # 🔥 BATASI UKURAN GAMBAR

st.markdown("""
<style>

.hero-title {
    font-size: 52px;
    font-weight: 800;
    line-height: 1.1;
    margin-top: 40px;
}

.hero-subtitle {
    font-size: 20px;
    color: #94A3B8;
    margin-top: 20px;
    line-height: 1.6;
    max-width: 600px;
}

</style>
""", unsafe_allow_html=True)
# ===============================
# MODE SELECTOR
# ===============================
st.markdown("<div class='card'>", unsafe_allow_html=True)

mode = st.radio(
    "Select Mode",
    ["Document Analyzer", "Financial Analyzer"]
)

st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# DOCUMENT ANALYZER
# ===============================
if mode == "Document Analyzer":

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload TXT or PDF file",
        type=["txt", "pdf"]
    )

    if uploaded_file:

        if uploaded_file.type == "text/plain":
            text = extract_text_from_txt(uploaded_file)

        elif uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)

        else:
            st.error("Unsupported file type")
            st.stop()

        if st.button("🚀 Analyze Document"):

            with st.spinner("🧠 AI is analyzing your document..."):

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an expert research assistant."},
                        {"role": "user", "content": f"Summarize this document clearly:\n\n{text[:12000]}"}
                    ]
                )

                summary = response.choices[0].message.content

                st.markdown("<div class='summary-box'>", unsafe_allow_html=True)
                st.markdown("### 📄 Summary Result")
                st.write(summary)
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# FINANCIAL ANALYZER
# ===============================
if mode == "Financial Analyzer":

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    finance_file = st.file_uploader(
        "Upload financial file (CSV / Excel)",
        type=["xlsx", "csv"],
        key="finance"
    )

    if finance_file:

        if finance_file.name.endswith(".csv"):
            df = pd.read_csv(finance_file)
        else:
            df = pd.read_excel(finance_file)

        st.success("File uploaded successfully!")
        st.dataframe(df.head())

        numeric_columns = df.select_dtypes(include="number").columns

        if len(numeric_columns) >= 2:

            revenue_col = numeric_columns[0]
            expense_col = numeric_columns[1]

            total_revenue = df[revenue_col].sum()
            total_expense = df[expense_col].sum()
            net_profit = total_revenue - total_expense

            profit_margin = (net_profit / total_revenue * 100) if total_revenue != 0 else 0

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Total Revenue", f"${total_revenue:,.2f}")
            col2.metric("Total Expense", f"${total_expense:,.2f}")
            col3.metric("Net Profit", f"${net_profit:,.2f}")
            col4.metric("Profit Margin", f"{profit_margin:.2f}%")

            if st.button("🧠 Generate AI Financial Insight"):

                summary_prompt = f"""
                Total Revenue: {total_revenue}
                Total Expense: {total_expense}
                Net Profit: {net_profit}
                Profit Margin: {profit_margin:.2f}%

                Provide professional financial insight and recommendation.
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a professional financial analyst."},
                        {"role": "user", "content": summary_prompt}
                    ]
                )

                ai_result = response.choices[0].message.content

                st.markdown("<div class='summary-box'>", unsafe_allow_html=True)
                st.markdown("### 🤖 AI Financial Insight")
                st.write(ai_result)
                st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.error("File must contain at least two numeric columns.")

    st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# FOOTER
# ===============================
st.markdown("""
<br><br>
<center style='color: #94A3B8;'>
AI Research & Finance Analyzer
</center>
""", unsafe_allow_html=True)