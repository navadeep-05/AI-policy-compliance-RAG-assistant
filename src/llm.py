import os             # Access environment variables
from dotenv import load_dotenv    # Load variables from .env
from google import genai  # Gemini API client

# Load variables from the .env file
load_dotenv()

# Read the Gemini API key
API_KEY = os.getenv("GEMINI_API_KEY")

# Create the Gemini client
client = genai.Client(api_key=API_KEY)

# Gemini model used for compliance analysis
MODEL_NAME = "gemini-3.8-flash"

def generate_compliance_assessment(proposal, evidence):
    # Build the policy evidence section
    evidence_text = ""

    for i, item in enumerate(evidence, start=1):
        evidence_text += f"""
Evidence {i}
Source: {item["source"]}
Page: {item["page"]}
Policy Text:
{item["text"]}
"""

    # Create the instruction for Gemini
    prompt = f"""
You are an AI Policy Compliance Assistant.

Analyze the employee proposal using ONLY the provided policy evidence.

Employee Proposal:
{proposal}

Policy Evidence:
{evidence_text}

Provide:

1. Compliance Status: Compliant, Non-Compliant, or Requires Approval
2. Reason: Brief explanation based on the policy
3. Evidence: Mention the relevant source and page
4. Recommended Action: What the employee should do

Do not invent policies or facts that are not present in the evidence.
"""

    # Send the prompt to Gemini
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    # Return Gemini's response text
    return response.text


if __name__ == "__main__":

    # Example employee proposal
    proposal = "I want to work remotely for 20 days using my personal laptop."

    # Example evidence from our retriever
    evidence = [
        {
            "text": "Standard remote work is permitted for up to 30 consecutive calendar days per year with manager approval.",
            "source": "remote_work_policy.pdf",
            "page": 1
        },
        {
            "text": "BYOD personal laptops are prohibited for remote operations exceeding 5 business days.",
            "source": "remote_work_policy.pdf",
            "page": 2
        }
    ]

    # Ask Gemini to assess the proposal
    result = generate_compliance_assessment(
        proposal,
        evidence
    )

    print("\nCompliance Assessment:\n")
    print(result)