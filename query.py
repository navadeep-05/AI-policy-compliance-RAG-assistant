from src.retriever import retrieve_and_rerank  # Retrieve and rerank policy evidence
from src.llm import generate_compliance_assessment  # Send evidence to Gemini


def process_policy_query(proposal):
    # Retrieve and rerank the most relevant policy evidence
    evidence = retrieve_and_rerank(
        proposal,
        retrieve_k=5,
        rerank_k=3
    )

    # Send the proposal and evidence to Gemini
    assessment = generate_compliance_assessment(
        proposal,
        evidence
    )

    # Return both evidence and final assessment
    return evidence, assessment


if __name__ == "__main__":

    # Example employee proposal
    proposal = (
        "I want to work remotely for 20 days "
        "using my personal laptop."
    )

    # Run the complete RAG pipeline
    evidence, assessment = process_policy_query(proposal)

    # Display the employee proposal
    print("\n" + "=" * 70)
    print("EMPLOYEE PROPOSAL")
    print("=" * 70)
    print(proposal)

    # Display the retrieved policy evidence
    print("\n" + "=" * 70)
    print("RETRIEVED POLICY EVIDENCE")
    print("=" * 70)

    for rank, item in enumerate(evidence, start=1):
        print(f"\n--- Evidence {rank} ---")
        print("Source:", item["source"])
        print("Page:", item["page"])
        print("Score:", item["score"])
        print("Text:", item["text"])

    # Display Gemini's compliance assessment
    print("\n" + "=" * 70)
    print("COMPLIANCE ASSESSMENT")
    print("=" * 70)
    print(assessment)