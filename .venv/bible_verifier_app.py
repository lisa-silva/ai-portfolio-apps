import streamlit as st
import requests
import json
import time
from typing import Dict, Any, List

# --- Configuration ---
# NOTE: The apiKey will be automatically injected by the execution environment
# when run in Canvas. For local testing, you would set your actual API key here.
API_KEY = ""
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"
MODEL_NAME = "gemini-2.5-flash-preview-05-20"
MAX_RETRIES = 5

# --- Core LLM Verification Function with Exponential Backoff ---

@st.cache_data(show_spinner=False)
def verify_biblical_claim(claim: str) -> Dict[str, Any]:
    """
    Sends a claim to the Gemini model with Google Search grounding enabled
    for factual verification against biblical texts and related doctrines.

    Args:
        claim: The user's input (belief, tradition, or verse).

    Returns:
        A dictionary containing the generated text and a list of sources.
    """
    
    # 1. Define the System Prompt
    # This instructs the LLM on its persona and objective.
    system_prompt = (
        "You are an impartial Biblical Verifier tool designed to help curious users "
        "verify the source or foundation of a religious claim, tradition, or specific verse. "
        "Your goal is to provide a straightforward, respectful, and fact-based response. "
        "When presented with a claim, analyze it using the provided search results and determine "
        "its relationship to standard biblical texts (e.g., Is it a direct quote? A tradition "
        "derived from specific verses? A doctrine outside of Sola Scriptura?). "
        "Always cite the source material (biblical references, historical context, or search sources). "
        "Keep the response concise and objective. Avoid theological debate."
    )

    # 2. Define the User Query
    user_query = (
        f"VERIFICATION QUERY: Analyze the following claim/belief and verify its source "
        f"(Bible text, tradition, or external doctrine). If it's a verse, provide the book/chapter/verse. "
        f"If it's a tradition, state its origin and biblical justification (if any).\n\n"
        f"CLAIM: '{claim}'"
    )
    
    # 3. Construct the Payload
    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "tools": [{"google_search": {}}],  # Enable Google Search for external grounding
        "systemInstruction": {"parts": [{"text": system_prompt}]},
    }

    headers = {'Content-Type': 'application/json'}
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(f"{API_URL}?key={API_KEY}", headers=headers, data=json.dumps(payload), timeout=30)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            
            result = response.json()
            candidate = result.get('candidates', [{}])[0]

            if not candidate:
                return {"text": "Error: Model returned an empty response candidate.", "sources": []}

            # Extract the generated text
            text = candidate.get('content', {}).get('parts', [{}])[0].get('text', "Verification failed: Could not extract generated text.")

            # Extract grounding sources (citations)
            sources = []
            grounding_metadata = candidate.get('groundingMetadata')
            if grounding_metadata and grounding_metadata.get('groundingAttributions'):
                sources = [
                    {"uri": attr.get('web', {}).get('uri'), "title": attr.get('web', {}).get('title')}
                    for attr in grounding_metadata['groundingAttributions']
                    if attr.get('web', {}).get('uri')
                ]
            
            return {"text": text, "sources": sources}

        except requests.exceptions.RequestException as e:
            if attempt < MAX_RETRIES - 1:
                delay = 2 ** attempt  # Exponential backoff (1s, 2s, 4s, 8s...)
                time.sleep(delay)
            else:
                return {"text": f"Error: Failed to connect to the verification service after {MAX_RETRIES} attempts. Details: {e}", "sources": []}
        except Exception as e:
            return {"text": f"An unexpected error occurred during API processing: {e}", "sources": []}
            

# --- Streamlit UI and Logic ---

def main():
    """Defines the layout and interactivity of the Streamlit app."""
    
    # Set up the page configuration
    st.set_page_config(
        page_title="Biblical Claim Verifier (Portfolio Project)", 
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.title("⚖️ Biblical Claim Verifier")
    st.markdown(
        """
        This tool helps you objectively check the foundation of religious claims, traditions, or specific Bible verses. 
        It's designed for genuine curiosity, offering a straightforward verification of whether a concept is a direct 
        Bible text, a biblically-derived tradition, or an external doctrine.
        
        *This is a portfolio project demonstrating Python (Streamlit) and Generative AI (Google Gemini API) integration.*
        ---
        """
    )
    
    # Example input placeholder text
    example_claims = [
        "Matthew 23:9",
        "The perpetual virginity of Mary",
        "Praying with the Rosary beads",
        "Justification is by faith alone (sola fide)"
    ]
    
    # Text Input for the user's query
    claim_input = st.text_input(
        "Enter a Bible Verse, Belief, or Tradition to Verify:",
        placeholder=f"E.g., '{example_claims[1]}'",
        key="user_claim_input"
    )

    # Button to trigger the verification
    if st.button("Verify Claim", type="primary"):
        if claim_input:
            # Show a temporary loading message
            with st.spinner("Analyzing claim and searching biblical context..."):
                # Call the core verification function
                verification_result = verify_biblical_claim(claim_input)
            
            # --- Display Results ---
            st.markdown("### 📝 Verification Result")
            
            if "Error" in verification_result['text']:
                st.error(verification_result['text'])
            else:
                # Display the LLM's verified text
                st.info(verification_result['text'])
                
                # Display Sources if available (for data analysis/grounding demonstration)
                sources = verification_result.get('sources', [])
                if sources:
                    st.markdown("---")
                    st.markdown("#### 📚 Grounding Sources (Citations)")
                    st.markdown(
                        """
                        The following sources were used by the Generative Model to ground this response. 
                        This demonstrates the use of factual retrieval via the Google Search grounding tool.
                        """
                    )
                    
                    source_markdown = ""
                    for i, source in enumerate(sources, 1):
                        source_markdown += f"- **[{i}]** [{source['title'] or 'Source Link'}]({source['uri']})\n"
                    
                    st.markdown(source_markdown)
                else:
                    st.caption("No external search sources were explicitly cited for this query.")
        else:
            st.warning("Please enter a claim or verse to begin the verification.")
            
    # --- Sidebar for Portfolio Context and Examples ---
    st.sidebar.header("About This App")
    st.sidebar.markdown(
        """
        **Goal:** Provide an objective, fact-based tool for clarifying the source of religious claims (Bible vs. Tradition/Doctrine).

        **Technology Stack:**
        - **Python:** Primary development language.
        - **Streamlit:** Fast, interactive web framework for the UI.
        - **Google Gemini API:** Used for complex natural language analysis and summarization.
        - **Google Search Grounding:** Ensures factual accuracy by using real-time search results to verify claims against the Bible and historical documents.
        """
    )
    
    st.sidebar.header("Try These Examples:")
    st.sidebar.code(f"Verse: {example_claims[0]}")
    st.sidebar.code(f"Belief: {example_claims[1]}")
    st.sidebar.code(f"Tradition: {example_claims[2]}")
    st.sidebar.code(f"Doctrine: {example_claims[3]}")

if __name__ == "__main__":
    main()
