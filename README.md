🏛️ Political Fact-Checker App
Project Overview: Specialized AI for Real-Time Verification

This application demonstrates the ability to transform a general-purpose Large Language Model (LLM) into a specialized, impartial fact-checking tool for current events and political claims. It is designed to mitigate LLM hallucination by relying on real-time data sources.
Core Features

    Real-Time Grounding: Integrates the Gemini API with Google Search Grounding to ensure all verification is based on current, verifiable, web-indexed data (e.g., the latest BLS reports, budget proposals, etc.).

    Structured Output: Uses a custom System Prompt to force the LLM to output a rigid, impartial analysis framework: Verification Status (TRUE, FALSE, or MISLEADING), Supporting Evidence, and Contradicting Evidence/Context.

    High-Impact Deployment: Fully developed using Python and deployed via Streamlit Cloud, showcasing proficiency in full-stack (lite) deployment and secure API secrets management.

🔗 Live Application

Test the Deployed App Here: https://ai-portfolio-apps-cbdegem29gdrszqhwsatps.streamlit.app/

Technologies Used

    Language: Python

    Framework: Streamlit

    AI/API: Google Gemini API (generateContent)

    Data Sourcing: Google Search Grounding Tool
