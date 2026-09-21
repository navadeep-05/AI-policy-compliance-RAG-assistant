from pathlib import Path
import streamlit as st  # Streamlit for the web interface
from query import process_policy_query  # Run the complete RAG pipeline

# Locate the application background image
BACKGROUND_IMAGE = Path("assets/ui background 2.png")

# Apply the background image to the Streamlit page and sidebar
if BACKGROUND_IMAGE.exists():
    st.markdown(
        f"""
        <style>
        /* Apply background to the entire application */
        .stApp {{
            background-image: linear-gradient( rgba(10, 14, 24, 0.45), rgba(10, 14, 24, 0.45) ), url("data:image/png;base64,{__import__('base64').b64encode( BACKGROUND_IMAGE.read_bytes() ).decode()}");
            background-size: cover;
            background-position: center top; /* Anchors the top of the image to the top of the window */
            background-attachment: fixed;
            font-family: 'Inter', -apple-system, sans-serif;
        }}
        
        /* Make the very top header area completely transparent */
        [data-testid="stHeader"] {{
            background-color: transparent !important;
            background-image: none !important;
        }}

        /* Sidebar layout customization */
        [data-testid="stSidebar"] {{
            background-color: transparent !important;
            background-image: none !important;
        }}
        [data-testid="stSidebar"] > div:first-child {{
            background-color: rgba(15, 20, 32, 0.55) !important;
            backdrop-filter: blur(12px);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }}

        /* Glassmorphism panel for the central workspace */
        .stMainBlockContainer {{
            background: rgba(16, 22, 36, 0.4);
            backdrop-filter: blur(8px);
            padding: 2.5rem 3rem !important;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            margin-top: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        }}

        /* Unified Button styling */
        div[data-testid="stButton"] button {{
            width: 100% !important;
            border-radius: 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            background-color: rgba(255, 255, 255, 0.05) !important;
            transition: all 0.3s ease;
        }}
        div[data-testid="stButton"] button:hover {{
            background-color: rgba(255, 255, 255, 0.12) !important;
            border-color: rgba(255, 255, 255, 0.25) !important;
            transform: translateY(-1px);
        }}

        /* Text Area adjustments */
        div[data-testid="stTextArea"] textarea {{
            background-color: rgba(10, 14, 24, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
            color: #f0f2f6 !important;
        }}
        div[data-testid="stTextArea"] textarea:focus {{
            border-color: #ff4b4b !important;
            box-shadow: 0 0 0 1px #ff4b4b !important;
        }}

        /* Streamlit Expander card formatting */
        div[data-testid="stExpander"] {{
            background-color: rgba(15, 21, 35, 0.5) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 10px !important;
            margin-bottom: 0.75rem !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )




# Display the application title
st.title("📋 AI Policy Compliance Assistant")

# Brief description of the application
st.write(
    "Enter an employee proposal to check it against company policies."
)


# Provide ready-made examples so users can try the system quickly
st.subheader("💡 Try an Example")

example_1 = "I want to work remotely for 20 days using my personal laptop."
example_2 = "I want to work remotely for 10 days using a company-issued laptop with manager approval."
example_3 = "I want to work remotely for 45 consecutive days."

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💻 Personal Laptop"):
        st.session_state.proposal = example_1

with col2:
    if st.button("🏠 Company Laptop"):
        st.session_state.proposal = example_2

with col3:
    if st.button("📅 45 Days"):
        st.session_state.proposal = example_3


# Keep the selected example inside the text area
if "proposal" not in st.session_state:
    st.session_state.proposal = ""

proposal = st.text_area(
    "Employee Proposal",
    value=st.session_state.proposal,
    placeholder="Example: I want to work remotely for 20 days using my personal laptop.",
    height=120
)

# Keep manually entered text available for the next interaction
st.session_state.proposal = proposal


# Run the compliance check when the button is clicked
if st.button("🔍 Check Compliance", type="primary"):

    # Make sure the user entered a proposal
    if not proposal.strip():
        st.warning("Please enter an employee proposal.")

    else:
        # Show progress while the RAG pipeline runs
        with st.spinner("Analyzing policy compliance..."):

            # Run retrieval, reranking, and LLM assessment
            evidence, assessment = process_policy_query(proposal)

        # Display the final Gemini assessment
        st.subheader("📊 Compliance Assessment")
        st.markdown(assessment)

        # Display the evidence used by the LLM
        st.subheader("📚 Policy Evidence")

        for rank, item in enumerate(evidence, start=1):

            # Create an expandable section for each evidence chunk
            with st.expander(
                f"Evidence {rank} — {item['source']} | Page {item['page']}"
            ):

                st.write("**Relevance Score:**", round(item["score"], 3))

                st.write("**Policy Text:**")
                st.write(item["text"])