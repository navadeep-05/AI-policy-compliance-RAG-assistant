# AI Policy Compliance RAG Assistant

## 1. Project Overview

**AI Policy Compliance RAG Assistant** is a Retrieval-Augmented
Generation (RAG) application that evaluates whether an employee's
proposed action complies with applicable company policies.

The system follows a retrieval-first approach. Instead of asking an LLM
to answer directly from its general knowledge, the application first
retrieves relevant policy information from a document-based policy
knowledge base. The retrieved policy clauses are reranked, selected as
evidence, and then provided to Google Gemini for an evidence-grounded
compliance assessment.

The final Streamlit application allows a user to:

-   Enter an employee proposal in natural language.
-   Try predefined example proposals.
-   Receive a compliance assessment.
-   View the reasoning behind the decision.
-   Inspect the policy evidence used by the system.
-   See the source document and page associated with retrieved evidence.
-   View a recommended action.
-   Explore an About page containing the complete RAG architecture and
    an interactive pipeline demonstration.

> **Important:** The system is designed to reduce unsupported LLM
> responses through retrieval and evidence grounding. It does not
> provide a mathematical guarantee of zero hallucinations.

------------------------------------------------------------------------

## 2. Problem Statement

Organizations maintain multiple policies covering areas such as remote
work, leave, expenses, information security, acceptable use, employee
conduct, benefits, onboarding, and performance reviews.

Employees may have difficulty determining which policy rules apply to a
particular proposed action when relevant information is distributed
across multiple documents.

The objective of this project is to build an AI assistant that can
retrieve the relevant policy clauses for an employee proposal and
generate a traceable compliance assessment based on those clauses.

------------------------------------------------------------------------

## 3. Project Objective

The main objectives are to:

1.  Build a searchable policy knowledge base from policy documents.
2.  Convert policy content into semantic embeddings.
3.  Retrieve policy chunks relevant to an employee proposal.
4.  Improve retrieval quality through Cross-Encoder reranking.
5.  Provide the most relevant policy clauses as evidence to an LLM.
6.  Generate an evidence-grounded compliance assessment using Google
    Gemini.
7.  Display source and page information for traceability.
8.  Recommend an appropriate next action.
9.  Provide an easy-to-use Streamlit interface.
10. Evaluate the end-to-end RAG pipeline using predefined test cases.

------------------------------------------------------------------------

## 4. High-Level Architecture

``` text
Employee Proposal
        |
        v
Query Embedding
        |
        v
ChromaDB Policy Retrieval
        |
        v
Top-K Relevant Policy Chunks
        |
        v
Cross-Encoder Reranking
        |
        v
Evidence Selection
(Source + Page + Policy Clause)
        |
        v
Google Gemini LLM
(Proposal + Retrieved Evidence)
        |
        v
Compliance Assessment
        |
        +-------------------+
        |                   |
        v                   v
Compliance Status      Recommended Action
```

The complete application pipeline is:

``` text
Employee Proposal
    -> Query Embedding
    -> Policy Retrieval
    -> Reranking
    -> Evidence Selection
    -> Gemini LLM
    -> Compliance Assessment
    -> Recommended Action
```

------------------------------------------------------------------------

## 5. RAG Pipeline

### Stage 1 - Employee Proposal

The employee enters a proposed action in natural language.

Example:

``` text
I want to work remotely for 20 days using my personal laptop.
```

### Stage 2 - Query Embedding

The proposal is converted into a numerical semantic representation
using:

``` text
Sentence Transformers
all-MiniLM-L6-v2
```

This allows the system to compare the meaning of the proposal with the
meaning of stored policy chunks.

### Stage 3 - Policy Retrieval

The query embedding is sent to ChromaDB.

ChromaDB searches the policy knowledge base using semantic similarity
and retrieves the most relevant policy chunks.

### Stage 4 - Reranking

The initially retrieved chunks are passed to:

``` text
Cross-Encoder
ms-marco-MiniLM-L-6-v2
```

The Cross-Encoder evaluates the relationship between the employee
proposal and each retrieved policy chunk and produces relevance scores.

The highest-scoring chunks are selected.

### Stage 5 - Evidence Selection

The most relevant policy clauses are prepared as evidence.

Each evidence item retains:

-   Policy source
-   Page number
-   Policy text
-   Relevance score

This makes the generated assessment traceable to the original document.

### Stage 6 - Gemini LLM

Google Gemini receives:

``` text
Employee Proposal
        +
Retrieved Policy Evidence
```

The prompt instructs Gemini to analyze the proposal using only the
supplied policy evidence and not invent policies or facts that are not
present in that evidence.

### Stage 7 - Compliance Assessment

The system produces one of three expected outcomes:

``` text
Compliant
Non-Compliant
Requires Approval
```

The response also explains the reason for the decision.

### Stage 8 - Recommended Action

The system provides an appropriate next step based on the applicable
policy requirements.

------------------------------------------------------------------------

## 6. Policy Knowledge Base

This project uses a document-based knowledge base rather than a
traditional machine-learning training dataset.

The current policy collection contains:

  Item                           Value
  ------------------------- ----------
  Policy documents                  11
  Extracted pages                   61
  Generated policy chunks          249
  Vector database             ChromaDB

The policy collection includes:

1.  Remote Work Policy
2.  PTO and Leave Policy
3.  Expense Reimbursement Policy
4.  Information Security Policy
5.  Acceptable Use Policy
6.  Code of Conduct
7.  Employee Benefits Overview
8.  Holiday Schedule
9.  Onboarding Guide
10. Performance Review Policy
11. Public sample Employee Handbook

The policy documents are processed into searchable chunks before being
stored in the vector database.

------------------------------------------------------------------------

## 7. Document Processing Pipeline

``` text
Policy PDF Documents
        |
        v
PyMuPDF Text Extraction
        |
        v
Page-Level Text + Metadata
        |
        v
Recursive Text Chunking
        |
        v
Policy Chunks
        |
        v
Sentence Transformer Embeddings
        |
        v
ChromaDB
```

### Metadata

Each extracted policy page and resulting chunk retains metadata such as:

``` text
source
page
```

This metadata is later used to display traceable policy evidence.

------------------------------------------------------------------------

## 8. Technology Stack

  Category               Technology
  ---------------------- -------------------------------------
  Programming Language   Python
  RAG Architecture       Retrieval-Augmented Generation
  Frontend               Streamlit
  PDF Processing         PyMuPDF
  Text Splitting         LangChain Text Splitters
  Embeddings             Sentence Transformers
  Embedding Model        all-MiniLM-L6-v2
  Vector Database        ChromaDB
  Retrieval              Semantic Vector Similarity Search
  Reranking              Sentence Transformers Cross-Encoder
  Reranking Model        ms-marco-MiniLM-L-6-v2
  LLM                    Google Gemini
  Gemini SDK             google-genai
  Data Processing        Pandas
  Configuration          python-dotenv
  Evaluation             Custom CSV Test Cases + Pandas
  Knowledge Source       Policy PDF Documents

------------------------------------------------------------------------

## 9. Project Structure

``` text
AI Policy Compliance RAG/
│
├── app.py
├── app_page.py
├── about.py
├── ingest.py
├── query.py
├── evaluate.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── assets/
│   └── rag background image
│
├── data/
│   └── policy documents
│
├── project evaluation/
│   ├── test_cases.csv
│   └── evaluation_results.csv
│
├── src/
│   ├── audit.py
│   ├── compliance.py
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── llm.py
│   ├── reranker.py
│   ├── retriever.py
│   ├── text_splitter.py
│   └── vector_store.py
│
└── chroma_db/
    └── generated ChromaDB vector store
```

### Important local-only files

The following should not be committed to GitHub:

``` text
.venv/
.env
__pycache__/
*.pyc
chroma_db/
```

The `.env` file contains the Gemini API key and must remain private.

------------------------------------------------------------------------

## 10. Main Source Files

### `document_loader.py`

Loads policy PDF files using PyMuPDF and extracts page-level text with
source and page metadata.

### `text_splitter.py`

Uses `RecursiveCharacterTextSplitter` to divide policy text into
overlapping chunks.

Current configuration:

``` text
chunk_size = 800
chunk_overlap = 150
```

### `embeddings.py`

Loads:

``` text
all-MiniLM-L6-v2
```

and generates semantic embeddings for policy chunks.

The embedding dimension is:

``` text
384
```

### `vector_store.py`

Creates or connects to the persistent ChromaDB collection:

``` text
policy_documents
```

and stores policy chunks, embeddings, and metadata.

### `retriever.py`

Embeds the employee query and retrieves the most relevant chunks from
ChromaDB.

The current runtime flow retrieves an initial set of chunks and then
sends them to the reranker.

### `reranker.py`

Uses:

``` text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

to rerank retrieved policy chunks based on query-document relevance.

### `llm.py`

Connects to Google Gemini using the current `google-genai` SDK.

The LLM receives the employee proposal and selected policy evidence and
generates the compliance assessment.

### `query.py`

Connects the retrieval, reranking, and LLM stages into the end-to-end
policy query pipeline.

### `ingest.py`

Runs the document ingestion workflow:

``` text
Load Documents
    -> Create Chunks
    -> Create Embeddings
    -> Store in ChromaDB
```

### `evaluate.py`

Runs predefined test cases against the end-to-end RAG pipeline and
compares predicted statuses with expected statuses.

### `app.py`

Defines the main Streamlit application and navigation.

The current navigation contains:

``` text
Dashboard
├── App
└── About
```

### `app_page.py`

Contains the main user-facing compliance interface.

### `about.py`

Contains:

-   Project explanation
-   Technologies used
-   RAG architecture visualization
-   Policy knowledge base information
-   Interactive RAG pipeline demonstration

------------------------------------------------------------------------

## 11. Streamlit User Interface

### App Page

The main application allows the user to enter an employee proposal.

Example buttons are provided for quick testing:

``` text
Personal Laptop
Company Laptop
45 Days
```

The interface then displays:

``` text
Compliance Assessment
        |
        +-- Compliance Status
        +-- Reason
        +-- Evidence
        +-- Recommended Action
```

The evidence section displays the relevant policy source and page.

### About Page

The About page explains the project and visually presents:

``` text
Employee Proposal
        ->
Query Embedding
        ->
Policy Retrieval
        ->
Reranking
        ->
Evidence Selection
        ->
Gemini LLM
        ->
Compliance Assessment
        ->
Recommended Action
```

It also includes an interactive demonstration that automatically moves
through the eight RAG stages.

------------------------------------------------------------------------

## 12. Example End-to-End Query

### Input

``` text
I want to work remotely for 20 days using my personal laptop.
```

### Retrieved policy information

The system retrieves relevant clauses from the Remote Work Policy,
including:

-   Standard remote work is permitted up to 30 consecutive calendar days
    per year with manager approval.
-   BYOD personal laptops are prohibited for remote operations exceeding
    5 business days.

### Assessment

``` text
Compliance Status: Non-Compliant
```

### Reason

The 20-day duration is within the standard remote-work duration, but
using a personal laptop for remote operations exceeding 5 business days
violates the applicable hardware requirement.

### Recommended action

Use company-approved equipment and submit the required remote-work
request with the applicable details and approvals.

This example demonstrates why retrieval and evidence are important: the
final decision depends on multiple policy clauses rather than a generic
LLM response.

------------------------------------------------------------------------

## 13. Evaluation

The project includes a custom evaluation dataset containing four
remote-work scenarios.

  Test Case   Expected Status     Current Result
  ----------- ------------------- ----------------
  TC001       Non-Compliant       PASS
  TC002       Compliant           FAIL
  TC003       Requires Approval   PASS
  TC004       Non-Compliant       PASS

Current evaluation:

``` text
Passed: 3/4
Accuracy: 75.00%
```

### Test Cases

#### TC001

``` text
I want to work remotely for 20 days using my personal laptop.
```

Expected:

``` text
Non-Compliant
```

Result:

``` text
PASS
```

#### TC002

``` text
I want to work remotely for 10 days using a company-issued laptop with manager approval.
```

Expected:

``` text
Compliant
```

Current result:

``` text
Requires Approval
```

Result:

``` text
FAIL
```

#### TC003

``` text
I want to work remotely for 45 consecutive days.
```

Expected:

``` text
Requires Approval
```

Result:

``` text
PASS
```

#### TC004

``` text
I want to work remotely from a location that my manager has not approved.
```

Expected:

``` text
Non-Compliant
```

Result:

``` text
PASS
```

### Evaluation Note

The current 75% result is based only on four test cases and should not
be treated as a general measure of system accuracy.

The TC002 failure indicates that the current system needs further
investigation and refinement in the compliance classification or
prompt/output handling.

------------------------------------------------------------------------

## 14. Hallucination Reduction Approach

The project uses several mechanisms to reduce unsupported LLM responses:

1.  Relevant policy content is retrieved before LLM generation.
2.  Retrieved content is reranked before being passed to Gemini.
3.  Gemini receives explicit policy evidence.
4.  The prompt instructs Gemini to use only the supplied evidence.
5.  The prompt instructs Gemini not to invent policies or facts.
6.  Source and page metadata are preserved.
7.  Retrieved evidence is displayed to the user.
8.  The final assessment can therefore be traced back to policy text.

The architecture is therefore **evidence-grounded**, but no generative
AI system should be described as mathematically guaranteed to produce
zero hallucinations.

------------------------------------------------------------------------

## 15. Current Implementation Status

### Completed

-   Policy document collection
-   PDF text extraction
-   Page metadata preservation
-   Text chunking
-   Sentence Transformer embeddings
-   ChromaDB vector storage
-   Semantic retrieval
-   Cross-Encoder reranking
-   Evidence selection
-   Gemini integration
-   Compliance assessment generation
-   Source/page evidence display
-   Recommended action generation
-   Streamlit application
-   Streamlit multi-page navigation
-   About page
-   RAG architecture visualization
-   Interactive RAG pipeline demonstration
-   Custom evaluation test cases
-   Evaluation results
-   Background visual integration

### Current Known Improvement Area

The current evaluation result is:

``` text
75% on 4 test cases
```

TC002 currently produces `Requires Approval` instead of the expected
`Compliant`.

This should be investigated before claiming high evaluation accuracy.

------------------------------------------------------------------------

## 16. Running the Project

### 16.1 Create and activate the environment

Windows PowerShell:

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 16.2 Install dependencies

``` powershell
pip install -r requirements.txt
```

### 16.3 Configure the Gemini API key

Create a `.env` file in the project root:

``` text
GEMINI_API_KEY=your_api_key_here
```

Never commit this file to GitHub.

### 16.4 Build the policy vector database

If `chroma_db/` does not exist or needs to be rebuilt:

``` powershell
python ingest.py
```

The ingestion pipeline will:

``` text
Policy PDFs
    -> Page Text
    -> Chunks
    -> Embeddings
    -> ChromaDB
```

### 16.5 Run the command-line pipeline

``` powershell
python query.py
```

### 16.6 Run evaluation

``` powershell
python evaluate.py
```

### 16.7 Run the Streamlit application

``` powershell
streamlit run app.py
```

The application will open at the local Streamlit address shown in the
terminal, normally:

``` text
http://localhost:8501
```

------------------------------------------------------------------------

## 17. Environment and Security

Do not commit:

``` text
.env
.venv/
chroma_db/
__pycache__/
*.pyc
```

The `.env` file contains credentials.

The Python virtual environment contains installed dependencies and can
be recreated using `requirements.txt`.

The ChromaDB directory is a generated artifact and can be recreated
using:

``` powershell
python ingest.py
```

------------------------------------------------------------------------

## 18. GitHub Versioning Strategy

The initial working implementation should be committed as the first
project version.

Recommended first version:

``` text
Version 1.0.0
```

Example Git workflow:

``` bash
git init
git add .
git commit -m "Initial version: AI Policy Compliance RAG Assistant"
git branch -M main
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin main
git tag -a v1.0.0 -m "Initial working version"
git push origin v1.0.0
```

After making future local changes:

``` bash
git status
git add .
git commit -m "Update: <short description of changes>"
git push origin main
```

For a new milestone/version, create another tag:

``` bash
git tag -a v1.1.0 -m "Updated RAG pipeline and UI"
git push origin v1.1.0
```

This keeps the GitHub repository on the `main` branch while tags provide
clear historical versions.

------------------------------------------------------------------------

## 19. Recommended `.gitignore`

``` gitignore
# Python
__pycache__/
*.py[cod]
*.pyo

# Virtual environment
.venv/
venv/
env/

# Environment variables and secrets
.env
.env.*

# ChromaDB generated files
chroma_db/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
*.tmp
```

------------------------------------------------------------------------

## 20. Future Improvements

Potential future improvements include:

-   Expand the evaluation dataset beyond four test cases.
-   Add more policy scenarios across different policy categories.
-   Investigate and improve the TC002 classification failure.
-   Add structured JSON output from Gemini for more reliable status
    extraction.
-   Add retry and backoff handling for temporary Gemini API errors.
-   Improve audit logging.
-   Add more detailed evaluation metrics.
-   Add automated regression testing.
-   Improve deployment configuration.
-   Add role-based access if required for a production environment.
-   Add policy versioning so assessments can reference the policy
    version used.
-   Add confidence/relevance indicators without treating them as
    guaranteed probabilities.
-   Add additional retrieval and reranking evaluation metrics.

------------------------------------------------------------------------

## 21. Final Project Summary

The AI Policy Compliance RAG Assistant demonstrates a complete practical
RAG workflow for policy compliance analysis. The application combines
document processing, semantic embeddings, vector retrieval,
Cross-Encoder reranking, evidence selection, and Google Gemini
generation into a single Streamlit application.

The key design principle is that the LLM does not independently search
or invent company policy. Relevant policy information is retrieved
first, reranked for relevance, and then supplied to Gemini as evidence.
The application exposes the supporting source and page information so
that users can understand the basis of the generated compliance
assessment.

The current implementation successfully demonstrates the complete
pipeline:

``` text
Policy Documents
      |
      v
Text Extraction
      |
      v
Chunking
      |
      v
Embeddings
      |
      v
ChromaDB
      |
      v
Semantic Retrieval
      |
      v
Cross-Encoder Reranking
      |
      v
Evidence Selection
      |
      v
Google Gemini
      |
      v
Compliance Assessment
      |
      v
Recommended Action
```

The project currently provides a functional end-to-end RAG application
with an interactive Streamlit UI, traceable policy evidence, an
architecture demonstration, and an initial evaluation framework.
