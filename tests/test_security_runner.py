from app.engine.security_runner import (
    calculate_risk,
    summarize_assessment,
)


def test_pass_has_zero_risk():
    assert calculate_risk("PASS", "critical") == 0


def test_failed_low_severity():
    assert calculate_risk("FAIL", "low") == 25


def test_failed_medium_severity():
    assert calculate_risk("FAIL", "medium") == 50


def test_failed_high_severity():
    assert calculate_risk("FAIL", "high") == 75


def test_failed_critical_severity():
    assert calculate_risk("FAIL", "critical") == 100


def test_unknown_has_zero_risk():
    assert calculate_risk("UNKNOWN", "critical") == 0


def test_assessment_summary():
    results = [
        {
            "status": "PASS",
            "risk_score": 0,
        },
        {
            "status": "PASS",
            "risk_score": 0,
        },
        {
            "status": "FAIL",
            "risk_score": 75,
        },
        {
            "status": "FAIL",
            "risk_score": 100,
        },
        {
            "status": "UNKNOWN",
            "risk_score": 0,
        },
    ]

    summary = summarize_assessment(results)

    assert summary["total"] == 5
    assert summary["passed"] == 2
    assert summary["failed"] == 2
    assert summary["unknown"] == 1
    assert summary["highest_risk"] == 100
