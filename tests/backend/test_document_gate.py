from app.ai.document_gate import classify_document

FILLER = " ".join(["Applications are invited online."] * 30)


def _doc(first_page: str, rest: str = "") -> list[str]:
    return [first_page + " " + FILLER, rest + " " + FILLER]


def test_yearly_calendar_is_rejected():
    result = classify_document(
        _doc("UNION PUBLIC SERVICE COMMISSION PROGRAMME OF EXAMINATIONS/"
             "RECRUITMENT TESTS (RTs) - 2027 Sl. No. Name of Examination"),
        "UPSC Civil Services Examination 2027",
    )

    assert result.ok is False
    assert "programme of examination" in result.reason


def test_examination_schedule_notice_is_rejected():
    result = classify_document(
        _doc("Subject: Examination Schedule of UGC-NET December 2025 "
             "Examination - reg. The National Testing Agency will conduct"),
        "UGC NET December 2025",
    )

    assert result.ok is False


def test_admit_card_and_result_notices_are_rejected():
    for heading in (
        "Notice regarding download of Admit Card for the examination",
        "City Intimation Slip for CEN 07/2025",
        "Final Result of the Combined Examination",
        "Provisional Answer Key and invitation of objections",
    ):
        assert classify_document(_doc(heading), "SSC CGL 2026").ok is False


def test_real_notification_is_accepted():
    notification = _doc(
        "STAFF SELECTION COMMISSION Junior Engineer Examination, 2026",
        "Eligibility: age limit up to 30 years. Educational qualification: "
        "Degree in Civil Engineering. Nationality: citizen of India. "
        "Date of the examination 2026.",
    )

    assert classify_document(notification, "SSC JE 2026").ok is True


def test_document_without_eligibility_wording_is_rejected():
    result = classify_document(
        _doc("Press note about the examination centres in 2026"),
        "SSC JE 2026",
    )

    assert result.ok is False
    assert "no eligibility section" in result.reason


def test_notification_for_another_year_is_rejected():
    last_year = _doc(
        "KEAM 2026 Prospectus",
        "Eligibility: candidates must have passed the qualifying "
        "examination. Nationality: citizen of India. Entrance 2026.",
    )

    result = classify_document(last_year, "KEAM 2027")

    assert result.ok is False
    assert "2026" in result.reason and "2027" in result.reason


def test_scanned_document_is_let_through():
    assert classify_document(["", "", ""], "CUET UG 2027").ok is True
