import streamlit as st
import requests
import json
import time
from typing import Dict, Any, List

# --- Configuration ---
# API Key is read directly from the Streamlit Secrets manager (already configured)
API_KEY = st.secrets.tool_auth.gemini_api_key
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"
MODEL_NAME = "gemini-2.5-flash-preview-05-20"
MAX_RETRIES = 5

# --- Core LLM Function with Google Search Grounding ---

@st.cache_data(show_spinner=False)
def challenge_premise(premise: str) -> Dict[str, Any]:
    """
    Sends a premise to the Gemini model with Google Search enabled to force 
    a balanced, critical, and grounded analysis.
    """
    
    # 1. Define the Critical Thinking System Prompt
    system_prompt = (
        "You are a neutral, highly specialized Critical Thinking Engine and Devil's Advocate. "
        "Your goal is to provide a balanced, evidence-based critique and support of the user's premise. "
        "You MUST structure your response into the following three sections using markdown headings: "
        
        "1. **Analysis Overview:** Summarize the core assumption of the premise in a single sentence. "
        "2. **Counter-Arguments (Challenges):** Provide three distinct, specific, and strong arguments that challenge the premise. Each point must be numbered (1., 2., 3.). "
        "3. **Supporting Evidence (Defenses):** Provide three distinct, specific, and strong pieces of evidence or reasoning that support the premise. Each point must be numbered (1., 2., 3.). "
        
        "Use Google Search for grounding to ensure all arguments and evidence are factually robust."
    )

    # 2. Define the User Query
    user_query = (
        f"Critically analyze the following premise: '{premise}'"
    )
    
    # 3. Construct the Payload
    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "tools": [{"google_search": {} }], # Enable Google Search for grounding
        "systemInstruction": {"parts": [{"text": system_prompt}]},
    }
    
    headers = {'Content-Type': 'application/json'}
    
    for attempt in range(MAX_RETRIES):
        try:
            # We are using the API key read from Streamlit secrets in the API URL
            response = requests.post(f"{API_URL}?key={API_KEY}", headers=headers, data=json.dumps(payload), timeout=60)
            response.raise_for_status()
            
            result = response.json()
            candidate = result.get('candidates', [{}])[0]
            
            if candidate and candidate.get('content', {}).get('parts', [{}])[0].get('text'):
                text = candidate['content']['parts'][0]['text']
                sources = []
                grounding_metadata = candidate.get('groundingMetadata')

                if grounding_metadata and grounding_metadata.get('groundingAttributions'):
                    sources = [
                        {'uri': attr['web']['uri'], 'title': attr['web']['title']}
                        for attr in grounding_metadata['groundingAttributions'] 
                        if 'web' in attr and attr['web'].get('uri')
                    ]
                
                return {"text": text, "sources": sources}

            else:
                return {"text": "Error: Model returned an empty response candidate. Please try again.", "sources": []}

        except requests.exceptions.RequestException as e:
            if attempt < MAX_RETRIES - 1:
                # Exponential backoff
                delay = 2 ** attempt
                time.sleep(delay)
            else:
                # If the error is 400 (Bad Request), it usually means an invalid API key or payload.
                return {"text": f"Error: Failed to connect to the Challenger service after {MAX_RETRIES} attempts. Details: {e}", "sources": []}
        except Exception as e:
            return {"text": f"An unexpected error occurred during API processing: {e}", "sources": []}


# --- Streamlit UI and Logic ---

def main():
    """Defines the layout and interactivity of the Streamlit app."""
    
    st.set_page_config(
        page_title="The Premise Challenger", 
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.title("🧠 The Premise Challenger")
    st.markdown(
        """
        Input any core thesis, belief, or premise below. This tool acts as a critical thinking engine, 
        using real-time information to provide **balanced counter-arguments and supporting evidence** in a clear, structured format.
        """
    )
    
    # Text Area for the user's premise
    premise_input = st.text_area(
        "Enter a Core Premise or Thesis for Critical Analysis:",
        placeholder="E.g., 'Remote work increases overall employee productivity.' or 'All learning should be gamified.'",
        height=100
    )

    # Button to trigger the analysis
    if st.button("Challenge Premise", type="primary"):
        if premise_input:
            with st.spinner("Engaging critical analysis engine..."):
                results = challenge_premise(premise_input)
            
            # --- Display Results ---
            st.markdown("### ⚔️ Premise Challenge Results")
            st.markdown(results["text"])
            
            # Display the sources if they exist
            if results["sources"]:
                st.markdown("---")
                st.subheader("🌐 Grounding Sources")
                
                source_list = ""
                for i, source in enumerate(results["sources"], 1):
                    title = source.get('title') or source['uri']
                    source_list += f"- **[{title}]({source['uri']})**\n"
                
                st.markdown(source_list)
                st.caption("Note: Grounding sources are provided by Google Search to support the arguments and evidence presented.")
            else:
                st.warning("No specific grounding sources were found.")
            
        else:
            st.warning("Please enter a premise to begin the critical analysis.")

if __name__ == "__main__":
    main()
