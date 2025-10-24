# This is the Master Portfolio Dashboard file (app.py)
# It organizes and runs all six individual projects using a sidebar menu.

import streamlit as st
import pandas as pd
import io
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import datetime
from datetime import timedelta 
import time 

# --- NEW GLOBAL IMPORTS FOR PROJECTS 5 & 6 (FIXED ERRORS) ---
import sqlite3
import plotly.express as px 
# -----------------------------------------------------------

# --- Configuration ---
st.set_page_config(
    page_title="Lisa Silva Portfolio",
    layout="wide"
)

# --- Project Function Definitions (Containers) ---

def welcome_page():
    """The initial landing page of the portfolio."""
    st.title("⭐️ Capstone Portfolio Dashboard")
    st.subheader("Lisa Silva: Data Science & Application Development")
    
    st.markdown("""
        Welcome to my unified portfolio dashboard! This single application demonstrates a comprehensive range of skills 
        including **data processing (Pandas), web scraping, natural language processing (TextBlob), financial tracking, and AI integration.**
        
        Use the **sidebar menu** on the left to navigate between the six live applications.
    """)
    
    st.info("💡 Status: Project 5 (Finance Tracker) and Project 6 (LeaseSync AI) are fully integrated! Use the sidebar to explore.")


def csv_analyzer_app():
    """Container for the CSV Data Analyzer project (Project 1)."""
    st.title("1. 📊 CSV Data Analyzer (Pandas)")
    
    # Placeholder for CSV Analyzer code
    st.info("Coming soon: Paste the complete code from your working 'streamlit_app.py' file here.")
    st.markdown("**(Placeholder for CSV Data Analyzer App)**")


def web_scraper_app():
    """Container for the Web Scraper project (Project 2)."""
    st.title("2. 🕸️ Web Scraper")
    
    # Placeholder for Web Scraper code
    st.info("Coming soon: Paste the complete code from your working Web Scraper file here.")
    st.markdown("**(Placeholder for Web Scraper App)**")


def sentiment_analyzer_app():
    """Container for the Sentiment Analyzer project (Project 3)."""
    st.title("3. 💬 Sentiment Analyzer (NLP)")
    
    # Placeholder for Sentiment Analyzer code
    st.info("Coming soon: Paste the complete code from your working Sentiment Analyzer file here.")
    st.markdown("**(Placeholder for Sentiment Analyzer App)**")


def dark_triad_quiz_app():
    """Container for the Dark Triad Detector Quiz project (Project 4)."""
    st.title("4. 🧠 Dark Triad Detector Quiz")
    
    # Placeholder for Quiz code
    st.info("Coming soon: Paste the complete code from your working Dark Triad Quiz file here.")
    st.markdown("**(Placeholder for Dark Triad Quiz App)**")


def finance_app_container():
    """Container for the Where's My Money? Tracker project (Project 5)."""
    
    # --- Start of FIXED Finance Tracker Code ---
    
    # Initialize session state for storing transactions if it doesn't exist
    if 'transactions' not in st.session_state:
        st.session_state.transactions = pd.DataFrame(
            columns=['Date', 'Type', 'Amount', 'Category', 'Description']
        )
        
    st.title("5. 💰 Where's My Money? (Transaction Tracker)")
    st.markdown("A simple tool to track income and expenses and view your running balance.")

    # --- 1. Add New Transaction Section ---
    st.header("1. Add New Transaction")
    
    # FIX 1: Radio button moved outside the form to update categories immediately
    transaction_type = st.radio("Type", ["Income", "Expense"], horizontal=True, key="transaction_type_radio")

    # Define categories based on the user's selection above
    if transaction_type == "Income":
        categories = ["Salary", "Investment", "Gift", "Other Income"]
    else:
        categories = ["Groceries", "Rent", "Utilities", "Transport", "Entertainment", "Other Expense"]

    
    with st.form("transaction_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # FIX 2: Compensate for UTC skew by subtracting 1 day (using datetime.timedelta)
            server_date_skew = datetime.date.today()
            corrected_date = server_date_skew - timedelta(days=1)
            date = st.date_input("Date", corrected_date)
        
        with col2:
            amount = st.number_input("Amount", min_value=0.01, format="%.2f")
            category = st.selectbox("Category", categories)
            
        with col3:
            description = st.text_input("Description (Optional)")

        submitted = st.form_submit_button("Record Transaction")

        if submitted:
            final_amount = amount if transaction_type == "Income" else -amount
            
            new_transaction = pd.DataFrame({
                'Date': [date.strftime("%Y-%m-%d")],
                'Type': [transaction_type],
                'Amount': [final_amount],
                'Category': [category],
                'Description': [description]
            })
            
            st.session_state.transactions = pd.concat(
                [st.session_state.transactions, new_transaction], 
                ignore_index=True
            )
            st.success("Transaction recorded successfully!")

    # --- 2. Summary and Dashboard Section ---
    st.header("2. Financial Summary")

    if not st.session_state.transactions.empty:
        df = st.session_state.transactions
        
        total_income = df[df['Type'] == 'Income']['Amount'].sum()
        total_expense = df[df['Type'] == 'Expense']['Amount'].sum()
        net_balance = total_income + total_expense
        
        col_m1, col_m2, col_m3 = st.columns(3)
        
        col_m1.metric("Total Income", f"${total_income:,.2f}", "Up")
        col_m2.metric("Total Expenses", f"${abs(total_expense):,.2f}", "Down")
        col_m3.metric("Net Balance", f"${net_balance:,.2f}", 
                      "Positive" if net_balance >= 0 else "Negative")

        st.subheader("Transaction History")
        st.dataframe(df.sort_values(by='Date', ascending=False), use_container_width=True)

        st.subheader("Expenses by Category")
        expense_df = df[df['Type'] == 'Expense']
        if not expense_df.empty:
            category_summary = expense_df.groupby('Category')['Amount'].sum().abs().sort_values(ascending=False)
            st.bar_chart(category_summary)
        else:
            st.info("No expenses recorded yet to show category breakdown.")
            
    else:
        st.info("No transactions recorded yet. Add one above!")
    # --- End of FIXED Finance Tracker Code ---


def leasesync_ai_container():
    """Container for the LeaseSync AI project (Project 6)."""
    
    # NOTE: Imports like sqlite3 and plotly.express are now handled globally at the top of app.py

    # Connect to database (fake for now)
    conn = sqlite3.connect("leases.db")

    # Sample lease data
    @st.cache_data
    def load_data():
        data = pd.DataFrame({
            "tenant_id": [1, 2, 3],
            "name": ["John Doe", "Jane Smith", "Bob Lee"],
            "lease_end": ["2026-01-15", "2025-11-30", "2025-12-20"],
            "rent": [2000, 1800, 2200],
            "status": ["Active", "Active", "Pending Renewal"]
        })
        return data

    # Predict renewal likelihood (simple rule-based AI)
    def predict_renewal(data):
        today = datetime.datetime.now() # Use datetime.datetime now that it's imported globally
        data["days_to_end"] = [(datetime.datetime.strptime(date, "%Y-%m-%d") - today).days for date in data["lease_end"]]
        data["renewal_chance"] = [80 if days < 60 else 50 for days in data["days_to_end"]]
        return data

    # App Content Start
    st.title("6. 🤖 LeaseSync AI (AI Integration & Data Analysis)")
    
    # Content starts here
    data = load_data()
    
    # Use tabs for the LeaseSync pages instead of the sidebar menu.
    tab1, tab2, tab3 = st.tabs(["Lease Overview", "Renewal Predictions", "Dashboard"])

    with tab1:
        st.header("Lease Management")
        st.table(data[["tenant_id", "name", "lease_end", "rent", "status"]])
        st.write("Upload new lease data (CSV):")
        uploaded_file = st.file_uploader("Choose file", type="csv")
        if uploaded_file:
            new_data = pd.read_csv(uploaded_file)
            st.table(new_data)

    with tab2:
        st.header("Renewal Predictions")
        data = predict_renewal(data)
        st.table(data[["tenant_id", "name", "lease_end", "renewal_chance"]])
        for index, row in data.iterrows():
            if row["renewal_chance"] > 60:
                st.success(f"Send renewal offer to {row['name']}!")
            else:
                st.warning(f"Follow up with {row['name']}.")

    with tab3:
        st.header("Lease Dashboard")
        fig = px.bar(data, x="name", y="rent", color="status", title="Rent by Tenant")
        st.plotly_chart(fig)
    # App Content End


# --- Main Navigation Logic ---

def main_app():
    """Controls the sidebar navigation and page routing."""
    
    # Dictionary mapping sidebar text to the function to run
    PAGES = {
        "⭐️ Welcome & Overview": welcome_page,
        "1. 📊 CSV Data Analyzer": csv_analyzer_app,
        "2. 🕸️ Web Scraper": web_scraper_app,
        "3. 💬 Sentiment Analyzer": sentiment_analyzer_app,
        "4. 🧠 Dark Triad Quiz": dark_triad_quiz_app,
        "5. 💰 Where's My Money? (Finance)": finance_app_container,
        "6. 🤖 LeaseSync AI (AI Integration)": leasesync_ai_container, 
    }

    st.sidebar.header("Portfolio Projects")
    
    # Creates the sidebar radio buttons for navigation
    selection = st.sidebar.radio("Go to:", list(PAGES.keys()))

    # Run the selected function
    page_function = PAGES[selection]
    page_function()

# Execute the main application function
if __name__ == "__main__":
    main_app()
