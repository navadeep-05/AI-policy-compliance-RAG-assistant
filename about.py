from pathlib import Path
import streamlit as st

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


# ---------------------------------------------------------
# Page Header
# ---------------------------------------------------------

st.title("ℹ️ About the AI Policy Compliance Assistant")

st.markdown(
    """
    **AI Policy Compliance Assistant** is an AI-powered
    Retrieval-Augmented Generation (RAG) system designed to help
    employees understand whether a proposed action complies with
    company policies.

    Instead of relying only on the language model's general knowledge,
    the system retrieves relevant policy clauses from a company policy
    knowledge base and provides an evidence-backed compliance assessment.

    The system identifies the compliance status, explains the relevant
    policy rules, shows supporting evidence, and recommends an appropriate
    next step.
    """
)


st.divider()


# =========================================================
# TECHNOLOGIES USED
# =========================================================

st.header("🛠️ Technologies Used")

st.write(
    "The application combines document processing, semantic retrieval, "
    "reranking, vector search, and a generative LLM."
)


technologies = [
    (
        "🐍 Python",
        "Core programming language used to build the RAG pipeline."
    ),
    (
        "🎈 Streamlit",
        "Interactive web interface for the compliance assistant."
    ),
    (
        "📄 PyMuPDF",
        "Extracts text and page information from policy PDFs."
    ),
    (
        "✂️ LangChain Text Splitters",
        "Splits policy documents into manageable chunks."
    ),
    (
        "🔢 Sentence Transformers",
        "Converts policy chunks and user queries into semantic embeddings."
    ),
    (
        "🗄️ ChromaDB",
        "Stores and retrieves policy embeddings using vector similarity."
    ),
    (
        "🎯 Cross-Encoder",
        "Reranks retrieved policy clauses based on query relevance."
    ),
    (
        "🤖 Google Gemini",
        "Analyzes retrieved evidence and generates the final assessment."
    ),
    (
        "📊 Pandas",
        "Used for evaluation and test-case analysis."
    ),
]


# Display technologies in three native Streamlit columns
for row_start in range(0, len(technologies), 3):

    row = technologies[row_start:row_start + 3]

    columns = st.columns(3)

    for index, (technology, description) in enumerate(row):

        with columns[index]:

            with st.container(border=True):

                st.subheader(technology)

                st.caption(description)


st.divider()


# =========================================================
# RAG PIPELINE ARCHITECTURE
# =========================================================

st.header("🔄 How the RAG Pipeline Works")

st.write(
    "The system follows a retrieval-first architecture. "
    "The employee proposal is converted into a semantic query, "
    "relevant policy information is retrieved and reranked, "
    "and the selected evidence is provided to Google Gemini "
    "for the final compliance assessment."
)


# These stages represent the actual implemented pipeline.
pipeline_steps = [
    {
        "number": 1,
        "icon": "👤",
        "title": "Employee Proposal",
        "component": "User Input",
        "description": (
            "The employee enters a proposed action in natural language."
        ),
    },
    {
        "number": 2,
        "icon": "🔢",
        "title": "Query Embedding",
        "component": "all-MiniLM-L6-v2",
        "description": (
            "The proposal is converted into a semantic vector."
        ),
    },
    {
        "number": 3,
        "icon": "🔎",
        "title": "Policy Retrieval",
        "component": "ChromaDB",
        "description": (
            "Relevant policy chunks are retrieved using semantic similarity."
        ),
    },
    {
        "number": 4,
        "icon": "🎯",
        "title": "Reranking",
        "component": "Cross-Encoder",
        "description": (
            "Retrieved policy chunks are ranked by relevance to the proposal."
        ),
    },
    {
        "number": 5,
        "icon": "📚",
        "title": "Evidence Selection",
        "component": "Top-K Evidence",
        "description": (
            "The most relevant policy clauses are selected as evidence."
        ),
    },
    {
        "number": 6,
        "icon": "🤖",
        "title": "Gemini LLM",
        "component": "Google Gemini",
        "description": (
            "Gemini analyzes the proposal using the retrieved policy evidence."
        ),
    },
    {
        "number": 7,
        "icon": "📋",
        "title": "Compliance Assessment",
        "component": "Decision",
        "description": (
            "The system determines the compliance status and explains why."
        ),
    },
    {
        "number": 8,
        "icon": "✅",
        "title": "Recommended Action",
        "component": "Next Step",
        "description": (
            "The system provides an appropriate recommended action."
        ),
    },
]


# ---------------------------------------------------------
# Helper: Display One Architecture Card
# ---------------------------------------------------------

def display_pipeline_card(column, step):
    """Display one pipeline stage using only Streamlit elements."""

    with column:

        with st.container(border=True):

            st.markdown(
                f"### {step['number']}. {step['icon']}"
            )

            st.subheader(step["title"])

            st.caption(
                f"**{step['component']}**"
            )

            st.write(
                step["description"]
            )


# ---------------------------------------------------------
# Architecture Row 1
# ---------------------------------------------------------
# Flow:
# 1 → 2 → 3 → 4

row1 = st.columns([4, 1, 4, 1, 4, 1, 4])


display_pipeline_card(
    row1[0],
    pipeline_steps[0]
)

with row1[1]:
    st.markdown("### ➜")

display_pipeline_card(
    row1[2],
    pipeline_steps[1]
)

with row1[3]:
    st.markdown("### ➜")

display_pipeline_card(
    row1[4],
    pipeline_steps[2]
)

with row1[5]:
    st.markdown("### ➜")

display_pipeline_card(
    row1[6],
    pipeline_steps[3]
)


# ---------------------------------------------------------
# Vertical Connection
# ---------------------------------------------------------
# Stage 4 continues downward to Stage 5.

arrow_columns = st.columns(7)

with arrow_columns[6]:
    st.markdown("### ⬇️")


# ---------------------------------------------------------
# Architecture Row 2
# ---------------------------------------------------------
# The second row flows from right to left:
#
# 8 ← 7 ← 6 ← 5
#
# Therefore the actual pipeline remains:
#
# 4 → 5 → 6 → 7 → 8

row2 = st.columns([4, 1, 4, 1, 4, 1, 4])


# Stage 8 is on the left
display_pipeline_card(
    row2[0],
    pipeline_steps[7]
)

with row2[1]:
    st.markdown("### ←")


# Stage 7
display_pipeline_card(
    row2[2],
    pipeline_steps[6]
)

with row2[3]:
    st.markdown("### ←")


# Stage 6
display_pipeline_card(
    row2[4],
    pipeline_steps[5]
)

with row2[5]:
    st.markdown("### ←")


# Stage 5 is on the right
display_pipeline_card(
    row2[6],
    pipeline_steps[4]
)


st.caption(
    "Pipeline flow: Employee Proposal → Embedding → Retrieval → "
    "Reranking → Evidence → Gemini → Assessment → Recommended Action"
)


st.divider()

# =========================================================
# POLICY KNOWLEDGE BASE
# =========================================================

st.header("📚 Policy Knowledge Base")

st.write(
    "The RAG system uses a document-based policy knowledge base "
    "rather than a traditional tabular dataset. Policy documents "
    "are converted into searchable chunks and used as the source "
    "of evidence for compliance analysis."
)


# ---------------------------------------------------------
# Dataset overview
# ---------------------------------------------------------

dataset_col1, dataset_col2, dataset_col3 = st.columns(3)


with dataset_col1:

    with st.container(border=True):

        st.metric(
            "Policy Documents",
            "11"
        )

        st.caption(
            "10 synthetic ACME policies + "
            "1 public sample employee handbook"
        )


with dataset_col2:

    with st.container(border=True):

        st.metric(
            "Extracted Pages",
            "61"
        )

        st.caption(
            "Text extracted from the policy PDFs"
        )


with dataset_col3:

    with st.container(border=True):

        st.metric(
            "Policy Chunks",
            "249"
        )

        st.caption(
            "Chunks created for semantic retrieval"
        )


# ---------------------------------------------------------
# Policy categories
# ---------------------------------------------------------

st.subheader("📑 Policy Areas Covered")

policy_areas = [
    "🏠 Remote Work",
    "🌴 PTO & Leave",
    "💰 Expense Reimbursement",
    "🔐 Information Security",
    "💻 Acceptable Use",
    "🤝 Code of Conduct",
    "🎁 Employee Benefits",
    "📅 Holiday Schedule",
    "🚀 Onboarding",
    "📈 Performance Reviews",
    "📘 Employee Handbook",
]


# Display policy areas in three columns
for row_start in range(0, len(policy_areas), 3):

    row = policy_areas[row_start:row_start + 3]

    columns = st.columns(3)

    for index, policy in enumerate(row):

        with columns[index]:

            st.info(policy)


# =========================================================
# INTERACTIVE RAG PIPELINE
# =========================================================

import time


st.header("▶️ Interactive RAG Pipeline")

st.write(
    "Run the demonstration to see how an employee proposal "
    "moves through the complete RAG workflow."
)


# ---------------------------------------------------------
# Example proposals
# ---------------------------------------------------------

demo_proposals = [
    "I want to work remotely for 20 days using my personal laptop.",
    (
        "I want to work remotely for 10 days using a company-issued "
        "laptop with manager approval."
    ),
    "I want to work remotely for 45 consecutive days.",
]


selected_proposal = st.selectbox(
    "Employee Proposal",
    demo_proposals,
    key="rag_demo_proposal"
)


# ---------------------------------------------------------
# Interactive state
# ---------------------------------------------------------

if "pipeline_running" not in st.session_state:
    st.session_state.pipeline_running = False

if "pipeline_completed" not in st.session_state:
    st.session_state.pipeline_completed = False


# ---------------------------------------------------------
# Pipeline controls
# ---------------------------------------------------------

start_col, reset_col, _ = st.columns([1.5, 1, 5])


with start_col:

    if st.button(
        "▶️ Start Demo",
        type="primary",
        key="start_rag_demo"
    ):

        st.session_state.pipeline_running = True
        st.session_state.pipeline_completed = False

        st.rerun()


with reset_col:

    if st.button(
        "🔄 Reset",
        key="reset_rag_demo"
    ):

        st.session_state.pipeline_running = False
        st.session_state.pipeline_completed = False

        st.rerun()


# =========================================================
# AUTOMATIC PIPELINE DEMONSTRATION
# =========================================================

if st.session_state.pipeline_running:

    # Create placeholders that will update during the demo
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    details_placeholder = st.empty()


    # Run through all eight pipeline stages
    for current_stage, step in enumerate(pipeline_steps):

        # -------------------------------------------------
        # Progress
        # -------------------------------------------------

        progress_value = (
            current_stage + 1
        ) / len(pipeline_steps)

        progress_placeholder.progress(
            progress_value,
            text=(
                f"Pipeline Stage "
                f"{current_stage + 1} of "
                f"{len(pipeline_steps)}"
            )
        )


        # -------------------------------------------------
        # Pipeline status
        # -------------------------------------------------

        with status_placeholder.container():

            st.subheader("Pipeline Status")

            status_columns = st.columns(
                len(pipeline_steps)
            )


            for index, stage in enumerate(pipeline_steps):

                with status_columns[index]:

                    if index < current_stage:

                        # Completed stage
                        with st.container(border=True):

                            st.success(
                                f"✓ {stage['number']}"
                            )

                            st.caption(
                                f"{stage['icon']} "
                                f"{stage['title']}"
                            )


                    elif index == current_stage:

                        # Currently active stage
                        with st.container(border=True):

                            st.info(
                                f"● {stage['number']}"
                            )

                            st.caption(
                                f"{stage['icon']} "
                                f"{stage['title']}"
                            )


                    else:

                        # Stage not reached yet
                        with st.container(border=True):

                            st.caption(
                                f"○ {stage['number']}"
                            )

                            st.caption(
                                f"{stage['icon']} "
                                f"{stage['title']}"
                            )


        # -------------------------------------------------
        # Current stage details
        # -------------------------------------------------

        with details_placeholder.container():

            st.divider()

            st.subheader(
                f"{step['icon']} {step['title']}"
            )

            description_col, component_col = st.columns(
                [2, 1]
            )


            with description_col:

                with st.container(border=True):

                    st.write(
                        step["description"]
                    )


            with component_col:

                with st.container(border=True):

                    st.caption("Component")

                    st.write(
                        step["component"]
                    )


            # Show stage-specific information
            if current_stage == 0:

                st.info(
                    f"**Employee Proposal**\n\n"
                    f"{selected_proposal}"
                )


            elif current_stage == 1:

                st.info(
                    "The proposal is converted into a "
                    "semantic vector representation."
                )


            elif current_stage == 2:

                st.info(
                    "ChromaDB searches the policy knowledge "
                    "base for semantically relevant policy chunks."
                )


            elif current_stage == 3:

                st.info(
                    "The Cross-Encoder reranks the retrieved "
                    "policy chunks according to their relevance."
                )


            elif current_stage == 4:

                st.info(
                    "The highest-ranked policy clauses are "
                    "selected as evidence for the Gemini LLM."
                )


            elif current_stage == 5:

                st.info(
                    "Google Gemini analyzes the employee proposal "
                    "using the retrieved policy evidence."
                )


            elif current_stage == 6:

                st.info(
                    "The system determines whether the proposal "
                    "is Compliant, Non-Compliant, or Requires Approval."
                )


            elif current_stage == 7:

                st.success(
                    "The system generates an appropriate "
                    "recommended action based on the applicable policy."
                )


        # Keep each stage visible briefly
        time.sleep(1.2)


    # -----------------------------------------------------
    # Completion
    # -----------------------------------------------------

    progress_placeholder.progress(
        1.0,
        text="Pipeline completed — 8 of 8 stages"
    )


    with details_placeholder.container():

        st.divider()

        st.success(
            "🎉 RAG pipeline demonstration completed successfully."
        )

        st.caption(
            "Employee Proposal → Embedding → Retrieval → "
            "Reranking → Evidence → Gemini → Assessment → "
            "Recommended Action"
        )


    # Stop the automatic loop after completion
    st.session_state.pipeline_running = False
    st.session_state.pipeline_completed = True