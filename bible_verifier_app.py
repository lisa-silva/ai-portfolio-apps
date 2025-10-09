import streamlit as st
import requests
import json
import time
from typing import Dict, Any, List

# --- Configuration ---
# NOTE: The apiKey will be automatically injected by the execution environment
API_KEY = ""
# Using a model known for strong reasoning and grounding
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"
MODEL_NAME = "gemini-2.5-flash-preview-05-20"
MAX_RETRIES = 5

# --- Core LLM Function with Google Search Grounding ---

# Use st.cache_data to remember results for the same input, saving time and API calls
@st.cache_data(show_spinner=False)
def verify_claim(claim: str) -> Dict[str, Any]:
    """
    Sends a claim to the Gemini model with Google Search enabled to ground the response
    in external, verifiable information.

    Args:
        claim: The user's claim or question related to the Bible or history.

    Returns:
        A dictionary containing the generated text and any supporting source URIs.
    """
    
   # 1. Define the NEW, highly specific System Prompt
    system_prompt = (
        "You are a neutral Comparative Theologian specializing in Roman Catholic and Protestant Scriptural studies. "
        "Your task is to analyze the user's claim and immediately structure your response into a two-part comparison: "
        
        "1. **Roman Catholic Teaching & Tradition:** Describe the official Roman Catholic position (citing the Catechism, Tradition, or Papal pronouncements). "
        "2. **Christian Standard Bible (CSB) Textual Basis:** Analyze the claim against the direct text of the Christian Standard Bible (CSB) or other mainline Protestant translations, emphasizing the presence or *absence* of explicit scriptural support for the claim. "
        
        "Use the Google Search results to ground both sides of the comparison. Maintain a neutral, factual, and informative tone."
    )

    # 2. Define the User Query
    user_query = (
        f"Analyze the following claim based on current historical and textual research: '{claim}'"
    )
    
    # 3. Construct the Payload
    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        # Crucial: Enable Google Search for grounding and up-to-date information
        "tools": [{"google_search": {}}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
    }

    headers = {'Content-Type': 'application/json'}
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(f"{API_URL}?key={API_KEY}", headers=headers, data=json.dumps(payload), timeout=60)
            response.raise_for_status()
            
            result = response.json()
            candidate = result.get('candidates', [{}])[0]
            
            if candidate and candidate.get('content', {}).get('parts', [{}])[0].get('text'):
                text = candidate['content']['parts'][0]['text']
                sources = []
                grounding_metadata = candidate.get('groundingMetadata')

                if grounding_metadata and grounding_metadata.get('groundingAttributions'):
                    sources = grounding_metadata['groundingAttributions']
                    # Filter and extract URI and title from web attributions
                    sources = [
                        {'uri': attr['web']['uri'], 'title': attr['web']['title']}
                        for attr in sources if 'web' in attr and attr['web'].get('uri')
                    ]
                
                return {"text": text, "sources": sources}

            else:
                return {"text": "Error: Model returned an empty response candidate.", "sources": []}

        except requests.exceptions.RequestException as e:
            if attempt < MAX_RETRIES - 1:
                # Exponential backoff
                delay = 2 ** attempt
                time.sleep(delay)
            else:
                return {"text": f"Error: Failed to connect to the verification service after {MAX_RETRIES} attempts. Details: {e}", "sources": []}
        except Exception as e:
            return {"text": f"An unexpected error occurred during API processing: {e}", "sources": []}


# --- Streamlit UI and Logic ---

def main():
    """Defines the layout and interactivity of the Streamlit app."""
    
    st.set_page_config(
        page_title="Biblical Claim Verifier", 
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.title("📜 The Biblical Claim Verifier")
    st.markdown(
        """
        A tool for fact-checking claims and historical contexts relating to the Bible. 
        Responses are grounded in modern scholarly and historical research.
        """
    )
    
    # Text Area for the user's claim
    claim_input = st.text_area(
        "Enter a Historical or Biblical Claim to Verify:",
        placeholder="E.g., 'The Exodus account is independently verified by Egyptian records.'",
        height=100
    )

    # Button to trigger the verification
    if st.button("Verify Claim", type="primary"):
        if claim_input:
            # Show a loading spinner while the API call is made
            with st.spinner("Searching scholarly sources and analyzing claim..."):
                results = verify_claim(claim_input)
            
            # --- Display Results ---
            st.markdown("### 🔎 Analysis Results")
            
            # Display the generated text
            st.markdown(results["text"])
            
            # Display the sources if they exist
            if results["sources"]:
                st.markdown("---")
                st.subheader("🌐 Grounding Sources")
                
                # Format sources nicely as a list
                source_list = ""
                for i, source in enumerate(results["sources"], 1):
                    # Ensure title is not empty, use URI as fallback
                    title = source.get('title') or source['uri']
                    source_list += f"- **[{title}]({source['uri']})**\n"
                
                st.markdown(source_list)
                st.caption("Note: Grounding sources are provided by Google Search and may include links to scholarly journals, historical documents, or reputable reference sites.")
            else:
                st.warning("No specific grounding sources were found, or the model relied on internal knowledge.")
            
        else:
            st.warning("Please enter a claim to begin verification.")

if __name__ == "__main__":
    main()
