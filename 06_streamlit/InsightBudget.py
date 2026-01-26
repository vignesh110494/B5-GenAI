import streamlit as st
import pandas as pd
import os
from fpdf import FPDF

# ---------------- CONFIG ----------------
st.set_page_config(page_title="InsightBudget", layout="wide")

BASE_DIR = r"C:\Users\vigne\Codebase\B5-GenAI\06_streamlit"
DATA_PATH = os.path.join(BASE_DIR, "input.xlsx")
FONT_PATH = os.path.join(BASE_DIR, "DejaVuSans.ttf")

# ---------------- HEADER ----------------
st.markdown( 
    """
    <h1 style="text-align:center;color:#1F618D;">
        📊 InsightBudget
    </h1>
    <p style="text-align:center;">Budget Analysis, Forecasting & Reporting</p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("📂 Upload Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    # Save file locally
    with open(DATA_PATH, "wb") as f:
        f.write(uploaded_file.getbuffer())

    df = pd.read_excel(DATA_PATH)
    st.success("✅ File uploaded successfully")

    # ---------------- DEPARTMENT FILTER ----------------
    st.subheader("🏢 Department Filter")

    departments = ["All"] + sorted(df["Department"].dropna().unique().tolist())
    selected_dept = st.selectbox("Select Department", departments)

    if selected_dept != "All":
        df = df[df["Department"] == selected_dept]

    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    # ---------------- VARIANCE CALCULATION ----------------
    df["Variance"] = df["Planned_Budget"] - df["Actual_Budget"]

    # ---------------- VARIANCE CHART ----------------
    st.subheader("📉 Budget vs Actual Variance")
    st.bar_chart(df.set_index("Month")["Variance"])

    # ---------------- VISUALIZATIONS ----------------
    st.subheader("📊 Visualizations")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Bar Chart"):
            st.bar_chart(df.set_index("Month")["Actual_Budget"])

    with col2:
        if st.button("📈 Line Chart"):
            st.line_chart(df.set_index("Month")["Actual_Budget"])

    with col3:
        if st.button("🔵 Scatter Plot"):
            st.scatter_chart(df[["Planned_Budget", "Actual_Budget"]])

    # ---------------- AI BUDGET INSIGHTS ----------------
    st.subheader("🧠 AI Budget Recommendations")

    total_variance = df["Variance"].sum()
    overspend_months = (df["Variance"] < 0).sum()

    insights = []

    if overspend_months > 4:
        insights.append("⚠ Frequent overspending detected. Introduce stricter approvals.")

    if total_variance > 0:
        insights.append("✅ Overall budget savings achieved. Reallocate surplus strategically.")
    else:
        insights.append("❌ Net budget overrun. Review high-cost months immediately.")

    insights.append("💡 Track department-wise KPIs monthly.")
    insights.append("📊 Improve forecasting using rolling averages.")

    for insight in insights:
        st.write(insight)

    # ---------------- FORECASTING ----------------
    st.subheader("📈 Next Year Budget Forecast")

    forecast = df.groupby("Month")["Actual_Budget"].mean() * 1.08
    st.line_chart(forecast)

    # ---------------- EXPORT SECTION ----------------
    st.subheader("📤 Export Reports")

    # ---------- EXCEL EXPORT ----------
    if st.button("📥 Export Excel"):
        export_df = df.copy()
        export_df["Forecasted_Next_Year"] = export_df["Actual_Budget"] * 1.08
        export_path = os.path.join(BASE_DIR, "budget_insights.xlsx")
        export_df.to_excel(export_path, index=False)
        st.success("✅ Excel exported successfully")

    # ---------- PDF EXPORT (UNICODE SAFE) ----------
    if st.button("📄 Export PDF"):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Set margins explicitly
        pdf.set_left_margin(15)
        pdf.set_right_margin(15)
        pdf.set_top_margin(15)

        # Add Unicode font (fpdf2)
        pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
        pdf.set_font("DejaVu", size=11)

        # Reset cursor safely
        pdf.set_x(15)

        # Title
        pdf.cell(0, 10, "📊 Budget Insights Report", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(6)

        # Fixed usable width
        page_width = pdf.w - pdf.l_margin - pdf.r_margin

        for insight in insights:
            pdf.set_x(pdf.l_margin)  # VERY IMPORTANT
            pdf.multi_cell(page_width, 8, insight)
            pdf.ln(1)

        pdf_path = os.path.join(BASE_DIR, "budget_report.pdf")
        pdf.output(pdf_path)

        st.success("✅ PDF exported successfully to the folder path (Unicode-safe)")


else:
    st.info("⬆ Upload an Excel file to start analysis")
