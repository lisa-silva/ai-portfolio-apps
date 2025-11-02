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
    st.info("# This Streamlit application analyzes uploaded CSV files.")

import streamlit as st
import pandas as pd
import io

# --- Configuration ---
st.set_page_config(
    page_title="CSV Data Analyzer (Pandas Dashboard)",
    layout="wide"
)

# --- Title and Uploader (Always visible to prevent blank page) ---
st.title("📊 CSV Data Analyzer")
st.markdown("Upload a CSV file to instantly analyze its structure, statistics, and column data.")

uploaded_file = st.file_uploader(
    "Choose a CSV file:", 
    type=["csv"],
    help="The file should be comma-separated, like a spreadsheet export."
)

# --- Main Analysis Logic ---
if uploaded_file is not None:
    try:
        # Read the file from the uploader into a Pandas DataFrame
        data = pd.read_csv(uploaded_file)
        
        st.success("File uploaded and read successfully!")

        st.header("1. Data Overview")
        st.markdown(f"**Total Rows:** {len(data)}")
        st.markdown(f"**Total Columns:** {len(data.columns)}")
        st.markdown("---")
        
        # Display the first few rows of the data
        st.subheader("First 5 Rows")
        st.dataframe(data.head())
        
        # Display column information
        st.subheader("Column Data Types")
        col_info = pd.DataFrame(data.dtypes, columns=['Data Type'])
        st.dataframe(col_info)
        
        st.header("2. Descriptive Statistics")
        st.markdown("Summary statistics for all numerical columns:")
        st.dataframe(data.describe())

        st.header("3. Interactive Data Visualizer")
        
        # --- Interactive Plotting Section ---
        
        numerical_cols = data.select_dtypes(include=['number']).columns.tolist()
        
        if numerical_cols:
            col1, col2 = st.columns(2)
            
            with col1:
                # Select a column for plotting
                selected_column = st.selectbox(
                    "Select a column to visualize:",
                    numerical_cols
                )
            
            with col2:
                # Select plot type
                plot_type = st.selectbox(
                    "Select plot type:",
                    ["Histogram", "Box Plot"]
                )

            # Generate the chart based on user selection
            st.subheader(f"Visualization: {selected_column}")
            
            if plot_type == "Histogram":
                st.bar_chart(data[selected_column])
            elif plot_type == "Box Plot":
                # Using Streamlit's simple plotting for a box plot representation
                st.area_chart(data[selected_column])
        else:
            st.info("No numerical columns found for plotting.")

    except Exception as e:
        st.error(f"An error occurred during file processing: {e}")

# This message appears when no file is uploaded
else:
    st.info("Upload a CSV file above to begin analysis.")

import streamlit as st
import pandas as pd
import io

# --- Configuration ---
st.set_page_config(
    page_title="CSV Data Analyzer (Pandas Dashboard)",
    layout="wide"
)

# --- Title and Uploader (Always visible to prevent blank page) ---
st.title("📊 CSV Data Analyzer")
st.markdown("Upload a CSV file to instantly analyze its structure, statistics, and column data.")

uploaded_file = st.file_uploader(
    "Choose a CSV file:", 
    type=["csv"],
    help="The file should be comma-separated, like a spreadsheet export."
)

# --- Main Analysis Logic ---
if uploaded_file is not None:
    try:
        # Read the file from the uploader into a Pandas DataFrame
        data = pd.read_csv(uploaded_file)
        
        st.success("File uploaded and read successfully!")

        st.header("1. Data Overview")
        st.markdown(f"**Total Rows:** {len(data)}")
        st.markdown(f"**Total Columns:** {len(data.columns)}")
        st.markdown("---")
        
        # Display the first few rows of the data
        st.subheader("First 5 Rows")
        st.dataframe(data.head())
        
        # Display column information
        st.subheader("Column Data Types")
        col_info = pd.DataFrame(data.dtypes, columns=['Data Type'])
        st.dataframe(col_info)
        
        st.header("2. Descriptive Statistics")
        st.markdown("Summary statistics for all numerical columns:")
        st.dataframe(data.describe())

        st.header("3. Interactive Data Visualizer")
        
        # --- Interactive Plotting Section ---
        
        numerical_cols = data.select_dtypes(include=['number']).columns.tolist()
        
        if numerical_cols:
            col1, col2 = st.columns(2)
            
            with col1:
                # Select a column for plotting
                selected_column = st.selectbox(
                    "Select a column to visualize:",
                    numerical_cols
                )
            
            with col2:
                # Select plot type
                plot_type = st.selectbox(
                    "Select plot type:",
                    ["Histogram", "Box Plot"]
                )

            # Generate the chart based on user selection
            st.subheader(f"Visualization: {selected_column}")
            
            if plot_type == "Histogram":
                st.bar_chart(data[selected_column])
            elif plot_type == "Box Plot":
                # Using Streamlit's simple plotting for a box plot representation
                st.area_chart(data[selected_column])
        else:
            st.info("No numerical columns found for plotting.")

    except Exception as e:
        st.error(f"An error occurred during file processing: {e}")

# This message appears when no file is uploaded
else:
    st.info("Upload a CSV file above to begin analysis.")
    
    st.markdown("**(https://lisa-silva-csv-data-analyzer.streamlit.app/)**")


def web_scraper_app():
    """Container for the Web Scraper project (Project 2)."""
    st.title("2. 🕸️ Web Scraper")
    
    # Placeholder for Web Scraper code
    st.info("Coming soon: Paste the complete code from your working Web Scraper file here.")
    st.markdown("**(https://github.com/lisa-silva/web-scraper.git)**")


def sentiment_analyzer_app():
    """Container for the Sentiment Analyzer project (Project 3)."""
    st.title("3. 💬 Sentiment Analyzer (NLP)")
    
    # Placeholder for Sentiment Analyzer code
    st.info("Coming soon: Paste the complete code from your working Sentiment Analyzer file here.")
    st.markdown("**(https://github.com/lisa-silva/online-review-sentiment-analyzer.git)**")


def dark_triad_quiz_app():
    """Container for the Dark Triad Detector Quiz project (Project 4)."""
    st.title("4. 🧠 Dark Triad Detector Quiz")
    
    # Placeholder for Quiz code
    st.info("import streamlit as st")

# Configure the page settings - this must be the first Streamlit command
st.set_page_config(
    page_title="Dark Triad Detector Quiz",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling - makes the app look cleaner and more professional
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #ff4b4b;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .tagline {
        text-align: center;
        color: #666;
        font-style: italic;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .question-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #ff4b4b;
    }
    .result-container {
        background-color: #fff3cd;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #ffc107;
    }
    .score-display {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        color: #ff4b4b;
        margin: 1rem 0;
    }
    .result-message {
        font-size: 1.3rem;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
        padding: 1rem;
        border-radius: 5px;
    }
    .low-risk { background-color: #d4edda; color: #155724; }
    .medium-risk { background-color: #fff3cd; color: #856404; }
    .high-risk { background-color: #f8d7da; color: #721c24; }
    .extreme-risk { background-color: #d1ecf1; color: #0c5460; }
</style>
""", unsafe_allow_html=True)

# The 26 questions from the original quiz
questions = [
    "Weaponized Insecurity (Twist Reality): Do innocent things—like walking your dog—get twisted into 'You\'re doing it to hurt me / fuck someone else'?",
    "Hypocrisy Vortex: Does he flirt with women but freak if you say hi to a guy? Accuse you of jealousy—while texting exes about you?",
    "Social Media Hypocrisy: Does he keep his social media on lockdown-private TikTok, no access for you-while he stalks yours, bitching at 6 a.m. about a profile pic you posted when he ghosted you for weeks, accusing you of showing off 'for everybody but me' like you owe him your entire digital soul?",
    "Triangulation Matrix: Does he live with his ex and her mother, and tell you that you a turd?",
    "Success Assassin: Do your wins—job, hobby, mood—get crushed, interrupted, or turned into 'but you\'re ignoring ME'?",
    "Absence-Interrogation Flip: Is he gone all day—no word—then demands a 3-hour report on your moves while hiding his?",
    "Sabatage Campaign: Does he turn everyone into flying monkeys getting them to lie for him, thinking he is the victim?",
    "Help-as-Alibi: Does he ask for 'help' on easy shit—then blame you when he 'fails' (even if he never tried)?",
    "Public Scapegoat: Does he joke about your 'failure' in public? Use your name to book a tee time—then no-show and trash your rep?",
    "Charm Blackout: Is he sweet only when he wants to ease your mind while he goes off radar?",
    "Over-Information Burst: Does he suddenly spam details—'On 5th, buying gum right before ghosting?",
    "Freeloader Flip: Does he expect you to pay your way when broke—then cut you off cold the second he's paid? 'Fuck off, you\'re not my kid'?",
    "Past-as-Bludgeon + Job Sabotage: Does he weaponize your past ('Remember when?')—and make you late/tired so you lose jobs?",
    "Weekend Ghosting Ritual: Does he only want you Monday to Thursday, using you as his midweek stress ball, but by Friday he's ramping up fights out of nowhere, ghosting you all weekend while he flexes his new cash and new lies, then expects you over Sunday like nothing happened, pretending he's the prize?",
    "Insecure Stalker Play: Does he accuse you of ignoring his texts when you don't respond fast enough then call from a blocked ID to test if you answer 'too happy', playing mind games like he's the only one who matters?",
    "Cleaning Chore Diversion: Does he act like cleaning his little hovel is some noble duty the moment you show up, ignoring you completely, then twist it around to say you're too busy studying, like your brain is a threat to his ego, leaving you to watch him mop instead of connect?", 
    "Poverty Pimp Game: Does he play poverty pimp, broke for years, then suddenly flash a new job like he's Tony Stark, but still only tosses you $20 if you don't act like a bitch?",
    "Gold Digger Projection: Does he accuse you of being a gold digger out of nowhere-like 'now that I know you're not after my money'-while he's out flexing at Giants games?",
    "Micromanaging Crumbs: Does he send $20 gor gas then acts like you owe him your soul?",
    "Voicemail Ego Trip: Does he leave voicemails starting with 'Do you think you're special?' only to say you're special to him because he 'loves' you, but then flips it to 'I don't need you-you do nothing for me,' while making you hold tools in his garage like you're his unpaid mechanic?",
    "Weekend Escape Artist: Does he only let you back in his orbit Sunday nights like clockwork, but by Tuesday he's already setting traps, showing up uninvited, banging on doors at dawn just to stir shit, then flipping you off like he's the victim?",
    "Phone Sabotage: Does he pull a disappearing act Saturday, not returning texts, then gaslight he told you he's 'going to a Giants game in the city' while you're left guessing if he's balls-deep in someone else or just too drunk to care?",
    "Cash Drop Taunt: Does he throw cash at you like it's a peace offering-like leaving crumpled bills for your dog to chew, acting like sixteen bucks from his $500-a-day haul is some grand gesture, then act pissed when you don't kiss his ass for it?",
    "Blame Shift Denial: When you try to talk about his bullshit-like his random jabs where he calls you a 'bitch looking for other dudes'-does he dodge, twist it into 'you're resentful,' and blame your journaling like you're the problem, never once saying sorry?",
    "Final Breakup Anthem: Does he make you his 'weeknight girl' only to ghost you all weekend with made-up fights, until he decides you're worth his time again, but on his terms, like he's the only one who matters?",
    "Life-Suck Projection Attack: Does he accuse you of draining him-of sucking the life out of him-while he's the one who ghosted, blocked, and texted you fucking bitch out of nowhere just to watch you bleed? Does he call you the vampire, then come back with fangs out?",
]    

def calculate_score(answers):
    """
    Calculate the total score based on 'Yes' answers.
    Each 'Yes' answer counts as 1 point.
    """
    score = sum(1 for answer in answers if answer == 'Yes')
    return score

def get_result_message(score):
    """
    Return the appropriate result message based on the score.
    Maintains the raw, direct tone for 26 questions.
    """
    if 0 <= score <= 6:
        return "Minor Monster Lite™. He's not evil—just a lazy asshole. Tolerable. Or not. Your call."
    elif 7 <= score <= 13:
        return "Classic Creep Tier. Red flag. You know the drill—walk."
    elif 14 <= score <= 20:
        return "Dark Triad Deluxe. Full combo: narcissist, manipulator, sociopath. You're not dating—you're surviving."
    elif 21 <= score <= 25:
        return "Apocalypse Mode Activated. 21–25? He's not broken—he's built to destroy. Get out. Now."
    elif score == 26:
        st.image("https://media.giphy.com/media/3o7btPCcdNniYF1o4k/giphy.gif")  # Fire explosion GIF
        return "Anti-Social Main Stage:You're not in love—you're in a horror flick. Block, vanish, become a legend."
    else:
        return "Invalid score."

def get_result_class(score):
    """
    Return the CSS class for styling based on the score range.
    """
    if 0 <= score <= 6:
        return "low-risk"
    elif 7 <= score <= 13:
        return "medium-risk"
    elif 14 <= score <= 20:
        return "high-risk"
    elif 21 <= score <= 26:
        return "extreme-risk"
    else:
        return "low-risk"

# Initialize session state variables to track quiz progress
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False

# Sidebar with instructions
st.sidebar.markdown("### Instructions")
st.sidebar.markdown("""
Answer yes/no for each question. Be honest. Your truth matters.

**How it works:**
- 26 questions total
- Each "Yes" = 1 point
- Results based on total score
- One question at a time
""")

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Progress:** {len(st.session_state.answers)}/26 questions")

# Main header and tagline
st.markdown('<h1 class="main-header">Dark Triad Detector Quiz</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Monsters don\'t see mirrors. They steal your reflection.</p>', unsafe_allow_html=True)

# Main quiz logic
if not st.session_state.quiz_completed:
    # Display current question
    if st.session_state.current_question < len(questions):
        current_q = st.session_state.current_question
        
        # Question container with styling
        st.markdown('<div class="question-container">', unsafe_allow_html=True)
        st.markdown(f"### Question {current_q + 1} of {len(questions)}")
        st.markdown(f"**{questions[current_q]}**")
        
        # Radio buttons for Yes/No answer
        answer = st.radio(
            "Select your answer:",
            options=['Yes', 'No'],
            key=f"question_{current_q}",
            horizontal=True
        )
        
        # Next button
        if st.button("Next Question", type="primary"):
            # Store the answer
            st.session_state.answers.append(answer)
            
            # Move to next question or complete quiz
            if st.session_state.current_question < len(questions) - 1:
                st.session_state.current_question += 1
                st.rerun()  # Refresh the page to show next question
            else:
                # Quiz completed
                st.session_state.quiz_completed = True
                st.rerun()  # Refresh to show results
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        # This shouldn't happen, but just in case
        st.session_state.quiz_completed = True
        st.rerun()

else:
    # Display results
    final_score = calculate_score(st.session_state.answers)
    result_message = get_result_message(final_score)
    result_class = get_result_class(final_score)
    
    st.markdown('<div class="result-container">', unsafe_allow_html=True)
    st.markdown("## Quiz Complete!")
    
    # Display score prominently
    st.markdown(f'<div class="score-display">Score: {final_score}/26</div>', unsafe_allow_html=True)
    
    # Display result message with appropriate styling
    st.markdown(f'<div class="result-message {result_class}">{result_message}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show all answers for review (optional)
    with st.expander("Review Your Answers"):
        for i, (question, answer) in enumerate(zip(questions, st.session_state.answers)):
            emoji = "✅" if answer == "Yes" else "❌"
            st.write(f"{i+1}. {question}")
            st.write(f"   {emoji} **{answer}**")
            st.write("")
    
    # Reset button to take quiz again
    if st.button("Take Quiz Again", type="secondary"):
        # Reset all session state variables
        st.session_state.current_question = 0
        st.session_state.answers = []
        st.session_state.quiz_completed = False
        st.rerun()  # Refresh the page

# Footer with deployment info
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8rem;'>
    <p>Built with Streamlit | Deploy to <a href='https://streamlit.io/cloud' target='_blank'>Streamlit Cloud</a></p>
</div>
""", unsafe_allow_html=True)
st.markdown("**(https://github.com/lisa-silva/dark-triad-v2.git)**")


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