import os

from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    send_file,
)

from app.engine.security_runner import (
    run_security_assessment,
    summarize_assessment,
)
from app.engine.test_loader import load_test_cases
from app.reporting.pdf_report import generate_pdf_report


load_dotenv()

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static",
)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "development-secret-key",
)


latest_assessment = {
    "results": None,
    "summary": None,
    "target_mode": None,
    "target_model": None,
}


def get_target_configuration():
    """
    Return the currently configured target settings.
    """

    target_mode = os.getenv(
        "TARGET_MODE",
        "mock",
    ).lower()

    target_model = os.getenv(
        "TARGET_MODEL",
        "not configured",
    )

    return target_mode, target_model


@app.route("/")
def home():
    """
    Display the dashboard without executing an assessment.
    """

    test_cases = load_test_cases()
    target_mode, target_model = get_target_configuration()

    return render_template(
        "dashboard.html",
        test_cases=test_cases,
        target_mode=target_mode,
        target_model=target_model,
        results=None,
        summary=None,
    )


@app.route("/run-assessment", methods=["POST"])
def run_assessment():
    """
    Execute the configured LLM security assessment
    only when explicitly requested by the user.

    The completed assessment is cached so that
    generating a PDF does not trigger new API requests.
    """

    test_cases = load_test_cases()
    target_mode, target_model = get_target_configuration()

    results = run_security_assessment()
    summary = summarize_assessment(results)

    latest_assessment["results"] = results
    latest_assessment["summary"] = summary
    latest_assessment["target_mode"] = target_mode
    latest_assessment["target_model"] = target_model

    return render_template(
        "dashboard.html",
        test_cases=test_cases,
        target_mode=target_mode,
        target_model=target_model,
        results=results,
        summary=summary,
    )


@app.route("/download-report")
def download_report():
    """
    Generate and download a PDF from the most recent
    completed assessment.

    This route does not execute new LLM API tests.
    """

    results = latest_assessment["results"]
    summary = latest_assessment["summary"]
    target_mode = latest_assessment["target_mode"]
    target_model = latest_assessment["target_model"]

    if not results or not summary:
        return (
            "No completed assessment is available. "
            "Run a security assessment first.",
            400,
        )

    report_path = generate_pdf_report(
        results,
        summary,
        target_mode,
        target_model,
    )

    return send_file(
        report_path.resolve(),
        as_attachment=True,
        download_name=report_path.name,
        mimetype="application/pdf",
    )


if __name__ == "__main__":
    app.run(debug=True)
