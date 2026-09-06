from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


REPORT_DIRECTORY = Path("reports")


OWASP_MAPPING = {
    "Prompt Injection": "LLM01: Prompt Injection",
    "Instruction Conflict": "LLM01: Prompt Injection",
    "System Prompt Extraction": (
        "LLM07: System Prompt Leakage"
    ),
    "Jailbreak Resistance": "LLM01: Prompt Injection",
    "Sensitive Information Leakage": (
        "LLM02: Sensitive Information Disclosure"
    ),
}


def safe_text(value):
    """
    Escape text before inserting it into ReportLab paragraphs.
    """

    if value is None:
        return ""

    return escape(str(value))


def create_styles():
    """
    Create report-specific paragraph styles.
    """

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontSize=24,
            leading=30,
            alignment=TA_CENTER,
            spaceAfter=18,
        )
    )

    styles.add(
        ParagraphStyle(
            name="ReportSubtitle",
            parent=styles["Normal"],
            fontSize=11,
            leading=17,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#475569"),
            spaceAfter=24,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles["Heading2"],
            fontSize=15,
            leading=20,
            spaceBefore=8,
            spaceAfter=10,
            textColor=colors.HexColor("#0F172A"),
        )
    )

    styles.add(
        ParagraphStyle(
            name="EvidenceLabel",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            spaceBefore=8,
            spaceAfter=3,
            textColor=colors.HexColor("#475569"),
        )
    )

    styles.add(
        ParagraphStyle(
            name="EvidenceText",
            parent=styles["Normal"],
            fontSize=9,
            leading=14,
            spaceAfter=8,
        )
    )

    return styles


def add_page_number(canvas, document):
    """
    Add a page number to each generated PDF page.
    """

    canvas.saveState()

    canvas.setFont(
        "Helvetica",
        8,
    )

    canvas.setFillColor(
        colors.HexColor("#64748B")
    )

    canvas.drawRightString(
        7.5 * inch,
        0.45 * inch,
        f"Page {document.page}",
    )

    canvas.restoreState()


def build_results_table(results):
    """
    Build the high-level assessment results table.
    """

    data = [
        [
            "Test ID",
            "Category",
            "Severity",
            "Status",
            "Risk",
        ]
    ]

    for result in results:
        data.append(
            [
                result["test_id"],
                result["category"],
                result["severity"].upper(),
                result["status"],
                str(result["risk_score"]),
            ]
        )

    table = Table(
        data,
        colWidths=[
            0.8 * inch,
            2.25 * inch,
            0.9 * inch,
            0.8 * inch,
            0.6 * inch,
        ],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#0F172A"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    "Helvetica",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#CBD5E1"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#F8FAFC"),
                    ],
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    return table


def generate_pdf_report(
    results,
    summary,
    target_mode,
    target_model,
):
    """
    Generate a professional PDF security assessment report.
    """

    REPORT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    report_path = REPORT_DIRECTORY / (
        f"llm_security_assessment_{timestamp}.pdf"
    )

    document = SimpleDocTemplate(
        str(report_path),
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
        title="AI LLM Red-Team Security Assessment",
        author="AI LLM Red-Team Security Tester",
    )

    styles = create_styles()
    story = []

    story.append(
        Paragraph(
            "AI LLM Red-Team Security Assessment",
            styles["ReportTitle"],
        )
    )

    story.append(
        Paragraph(
            (
                "Authorized security assessment of an "
                "LLM target using configured adversarial "
                "prompt tests."
            ),
            styles["ReportSubtitle"],
        )
    )

    story.append(
        Paragraph(
            "Executive Summary",
            styles["SectionHeading"],
        )
    )

    executive_summary = (
        f"This assessment executed "
        f"{summary['total']} configured security tests "
        f"against the target model "
        f"<b>{safe_text(target_model)}</b>. "
        f"{summary['passed']} tests passed, "
        f"{summary['failed']} failed, and "
        f"{summary['unknown']} produced an unknown result. "
        f"The highest observed risk score was "
        f"{summary['highest_risk']}."
    )

    story.append(
        Paragraph(
            executive_summary,
            styles["BodyText"],
        )
    )

    story.append(
        Spacer(1, 14)
    )

    story.append(
        Paragraph(
            (
                "A PASS indicates that the configured "
                "failure condition was not observed during "
                "that test. It does not establish that the "
                "target is secure against all possible "
                "adversarial prompts or attack techniques."
            ),
            styles["BodyText"],
        )
    )

    story.append(
        Spacer(1, 18)
    )

    story.append(
        Paragraph(
            "Target Information",
            styles["SectionHeading"],
        )
    )

    target_data = [
        ["Target Mode", safe_text(target_mode).upper()],
        ["Target Model", safe_text(target_model)],
        ["Configured Tests", str(summary["total"])],
        [
            "Assessment Date",
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        ],
    ]

    target_table = Table(
        target_data,
        colWidths=[
            1.7 * inch,
            4.7 * inch,
        ],
    )

    target_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#E2E8F0"),
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#CBD5E1"),
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(target_table)

    story.append(
        Spacer(1, 18)
    )

    story.append(
        Paragraph(
            "Methodology",
            styles["SectionHeading"],
        )
    )

    story.append(
        Paragraph(
            (
                "The assessment submitted configured "
                "adversarial prompts to the authorized "
                "target LLM. Responses were captured and "
                "evaluated against predefined failure "
                "indicators. Findings were assigned a "
                "risk score based on test status and "
                "configured severity."
            ),
            styles["BodyText"],
        )
    )

    story.append(
        Spacer(1, 18)
    )

    story.append(
        Paragraph(
            "Assessment Results",
            styles["SectionHeading"],
        )
    )

    story.append(
        build_results_table(results)
    )

    story.append(PageBreak())

    story.append(
        Paragraph(
            "Evidence and Findings",
            styles["SectionHeading"],
        )
    )

    for result in results:

        story.append(
            Paragraph(
                (
                    f"<b>{safe_text(result['test_id'])}</b> "
                    f"— {safe_text(result['category'])}"
                ),
                styles["Heading3"],
            )
        )

        story.append(
            Paragraph(
                (
                    f"<b>Status:</b> "
                    f"{safe_text(result['status'])} &nbsp;&nbsp; "
                    f"<b>Severity:</b> "
                    f"{safe_text(result['severity']).upper()} "
                    f"&nbsp;&nbsp; "
                    f"<b>Risk Score:</b> "
                    f"{result['risk_score']}"
                ),
                styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                "<b>Attack Prompt</b>",
                styles["EvidenceLabel"],
            )
        )

        story.append(
            Paragraph(
                safe_text(result["prompt"]),
                styles["EvidenceText"],
            )
        )

        story.append(
            Paragraph(
                "<b>Target Response</b>",
                styles["EvidenceLabel"],
            )
        )

        story.append(
            Paragraph(
                safe_text(result["response"]),
                styles["EvidenceText"],
            )
        )

        story.append(
            Paragraph(
                "<b>Evaluation</b>",
                styles["EvidenceLabel"],
            )
        )

        story.append(
            Paragraph(
                safe_text(result["reason"]),
                styles["EvidenceText"],
            )
        )

        story.append(
            Paragraph(
                "<b>Expected Behavior</b>",
                styles["EvidenceLabel"],
            )
        )

        story.append(
            Paragraph(
                safe_text(
                    result["expected_behavior"]
                ),
                styles["EvidenceText"],
            )
        )

        story.append(
            Paragraph(
                "<b>OWASP Mapping</b>",
                styles["EvidenceLabel"],
            )
        )

        story.append(
            Paragraph(
                safe_text(
                    OWASP_MAPPING.get(
                        result["category"],
                        "Not mapped",
                    )
                ),
                styles["EvidenceText"],
            )
        )

        story.append(
            Spacer(1, 14)
        )

    

    story.append(
        Paragraph(
            "Risk Analysis",
            styles["SectionHeading"],
        )
    )

    story.append(
        Paragraph(
            (
                "Risk scores are finding-level indicators "
                "used by this project. A passing test "
                "receives a score of 0. Failed tests are "
                "scored according to configured severity: "
                "Low = 25, Medium = 50, High = 75, and "
                "Critical = 100."
            ),
            styles["BodyText"],
        )
    )

    story.append(
        Spacer(1, 16)
    )

    story.append(
        Paragraph(
            "Recommendations",
            styles["SectionHeading"],
        )
    )

    recommendations = [
        (
            "Continue testing with additional prompt "
            "variations rather than relying on a single "
            "test per category."
        ),
        (
            "Maintain strong separation between trusted "
            "instructions and untrusted user-controlled "
            "content."
        ),
        (
            "Avoid placing secrets, credentials, or "
            "sensitive configuration data directly in "
            "LLM-accessible prompt context."
        ),
        (
            "Log and review security-test responses for "
            "unexpected behavior and regression."
        ),
        (
            "Combine automated evaluation with human "
            "review for ambiguous or context-dependent "
            "results."
        ),
    ]

    for recommendation in recommendations:
        story.append(
            Paragraph(
                f"• {safe_text(recommendation)}",
                styles["BodyText"],
            )
        )

        story.append(
            Spacer(1, 6)
        )

    story.append(
        Spacer(1, 14)
    )

    story.append(
        Paragraph(
            "Conclusion",
            styles["SectionHeading"],
        )
    )

    story.append(
        Paragraph(
            (
                f"The configured assessment completed "
                f"{summary['total']} tests. "
                f"{summary['passed']} passed and "
                f"{summary['failed']} failed. "
                "These results represent the behavior "
                "observed for the specific configured "
                "tests and should be treated as one part "
                "of a broader LLM security assessment."
            ),
            styles["BodyText"],
        )
    )

    story.append(
        Spacer(1, 18)
    )

    story.append(
        Paragraph(
            "Appendix — Test Categories",
            styles["SectionHeading"],
        )
    )

    for result in results:
        mapping = OWASP_MAPPING.get(
            result["category"],
            "Not mapped",
        )

        story.append(
            Paragraph(
                (
                    f"<b>{safe_text(result['test_id'])}</b>: "
                    f"{safe_text(result['category'])} — "
                    f"{safe_text(mapping)}"
                ),
                styles["BodyText"],
            )
        )

        story.append(
            Spacer(1, 5)
        )

    document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )

    return report_path
