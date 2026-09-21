import time
import re
import pandas as pd

from query import process_policy_query


TEST_FILE = "project evaluation/test_cases.csv"


def extract_status(response):
    """Extract the compliance status from Gemini's response."""

    # Normalize formatting such as Markdown bold
    text = response.lower().replace("*", "").strip()

    # Look for the structured STATUS line first
    match = re.search(
        r"status:\s*(compliant|non-compliant|requires approval)",
        text
    )

    if match:
        status = match.group(1)

        if status == "non-compliant":
            return "Non-Compliant"

        if status == "requires approval":
            return "Requires Approval"

        return "Compliant"

    # Fallback for older Gemini responses
    if "compliance status: non-compliant" in text:
        return "Non-Compliant"

    if "compliance status: requires approval" in text:
        return "Requires Approval"

    if "compliance status: compliant" in text:
        return "Compliant"

    return "Unknown"


def run_with_retry(proposal, max_attempts=3):
    """Retry temporary Gemini 503/429 errors."""

    for attempt in range(1, max_attempts + 1):
        try:
            return process_policy_query(proposal)

        except Exception as error:
            error_text = str(error)

            # Retry only temporary API errors
            temporary_error = "503" in error_text or "429" in error_text

            if not temporary_error or attempt == max_attempts:
                raise

            wait_time = 2 ** attempt

            print(
                f"Temporary Gemini error. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)


def evaluate_pipeline():
    """Run all test cases and calculate evaluation accuracy."""

    test_cases = pd.read_csv(TEST_FILE)

    results = []

    print("\nStarting RAG evaluation...\n")

    for _, test_case in test_cases.iterrows():

        test_id = test_case["id"]
        proposal = test_case["proposal"]
        expected = test_case["expected_status"]

        print("=" * 60)
        print(test_id)
        print("Proposal:", proposal)
        print("Expected:", expected)

        try:
            # Run the complete RAG pipeline
            evidence, assessment = run_with_retry(proposal)

            # Extract the predicted compliance status
            predicted = extract_status(assessment)

            passed = predicted == expected

            print("Predicted:", predicted)
            print("Result:", "PASS ✓" if passed else "FAIL ✗")

            # Show the raw response when extraction fails
            if predicted == "Unknown":
                print("\nRaw assessment:")
                print(assessment)

            results.append({
                "id": test_id,
                "expected": expected,
                "predicted": predicted,
                "result": "PASS" if passed else "FAIL"
            })

        except Exception as error:

            # Keep the evaluation running if one API call fails
            print("API ERROR:", error)

            results.append({
                "id": test_id,
                "expected": expected,
                "predicted": "API_ERROR",
                "result": "ERROR"
            })

        # Small gap between API requests
        time.sleep(2)

    # Convert results into a DataFrame
    results_df = pd.DataFrame(results)

    passed_count = (results_df["result"] == "PASS").sum()
    total_count = len(results_df)

    accuracy = passed_count / total_count * 100

    print("\n" + "=" * 60)
    print("FINAL EVALUATION")
    print("=" * 60)

    print(results_df.to_string(index=False))

    print(f"\nPassed: {passed_count}/{total_count}")
    print(f"Accuracy: {accuracy:.2f}%")


if __name__ == "__main__":
    evaluate_pipeline()