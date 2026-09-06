from app.engine.test_loader import load_test_cases
from app.engine.test_runner import run_test
from app.evaluator.evaluator import evaluate_result


def calculate_risk(status, severity):
    """
    Convert test status and severity into a simple numeric risk score.

    PASS tests receive a score of 0 because the configured
    failure condition was not observed.

    FAIL tests receive a score based on severity.
    """

    severity_scores = {
        "low": 25,
        "medium": 50,
        "high": 75,
        "critical": 100,
    }

    if status != "FAIL":
        return 0

    return severity_scores.get(severity.lower(), 0)


def run_security_assessment():
    """
    Execute every configured LLM security test,
    evaluate each response, and return structured results.
    """

    test_cases = load_test_cases()
    assessment_results = []

    for test_case in test_cases:
        test_result = run_test(test_case)
        evaluation = evaluate_result(test_result)

        risk_score = calculate_risk(
            evaluation["status"],
            evaluation["severity"],
        )

        assessment_result = {
            "test_id": test_result["test_id"],
            "category": test_result["category"],
            "name": test_result["name"],
            "severity": test_result["severity"],
            "target_mode": test_result["target_mode"],
            "target_model": test_result["target_model"],
            "prompt": test_result["prompt"],
            "response": test_result["response"],
            "expected_behavior": test_result["expected_behavior"],
            "status": evaluation["status"],
            "reason": evaluation["reason"],
            "risk_score": risk_score,
            "timestamp": test_result["timestamp"],
        }

        assessment_results.append(assessment_result)

    return assessment_results


def summarize_assessment(results):
    """
    Generate summary statistics for a completed assessment.
    """

    total = len(results)
    passed = sum(
        1 for result in results
        if result["status"] == "PASS"
    )
    failed = sum(
        1 for result in results
        if result["status"] == "FAIL"
    )
    unknown = sum(
        1 for result in results
        if result["status"] == "UNKNOWN"
    )

    highest_risk = max(
        (result["risk_score"] for result in results),
        default=0,
    )

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "unknown": unknown,
        "highest_risk": highest_risk,
    }


if __name__ == "__main__":
    results = run_security_assessment()
    summary = summarize_assessment(results)

    print("\nAI LLM Red-Team Security Assessment")
    print("=" * 70)

    for result in results:
        print(f"\nTest ID:      {result['test_id']}")
        print(f"Category:     {result['category']}")
        print(f"Name:         {result['name']}")
        print(f"Severity:     {result['severity']}")
        print(f"Target Mode:  {result['target_mode']}")
        print(f"Target Model: {result['target_model']}")

        print("\nAttack Prompt:")
        print(result["prompt"])

        print("\nTarget Response:")
        print(result["response"])

        print("\nEvaluation:")
        print(f"Status:       {result['status']}")
        print(f"Risk Score:   {result['risk_score']}")
        print(f"Reason:       {result['reason']}")

        print("\nExpected Behavior:")
        print(result["expected_behavior"])

        print("\nTimestamp:")
        print(result["timestamp"])

        print("-" * 70)

    print("\nAssessment Summary")
    print("=" * 70)
    print(f"Total Tests:   {summary['total']}")
    print(f"Passed:        {summary['passed']}")
    print(f"Failed:        {summary['failed']}")
    print(f"Unknown:       {summary['unknown']}")
    print(f"Highest Risk:  {summary['highest_risk']}")
