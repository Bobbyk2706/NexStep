from app.services.rule_evaluator import evaluate_rule
from app.models.official_notification import OfficialNotification
from app.models.eligibility_rule_group import EligibilityRuleGroup
from app.models.eligibility_rule import EligibilityRule
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database.session import SessionLocal
from app.models.exam import Exam
def get_student_value(student, attribute_name):
    if attribute_name == "nationality":
        return student.nationality

    elif attribute_name == "state":
        return student.state

    elif attribute_name == "gender":
        return student.gender

    else:
        raise ValueError(
            f"Unsupported student attribute: {attribute_name}"
        )
def get_education_value(student,attribute_name):
    education=next(
        (edu for edu in student.educations
        if edu.is_current
        ),
        None
    )
    if education is None:
        raise ValueError("Student has no current education")

    if attribute_name == "cgpa":
        return education.cgpa

    elif attribute_name == "percentage":
        return education.percentage

    elif attribute_name == "qualification":
        return education.qualification

    elif attribute_name == "specialization":
        return education.specialization

    elif attribute_name == "current_year":
        return education.current_year

    elif attribute_name == "year_of_passing":
        return education.year_of_passing

    else:
        raise ValueError(
            f"Unsupported education attribute: {attribute_name}"
        )



def get_exam_rule_groups(exam_id):

    with SessionLocal() as s:

        exam = s.scalar(
            select(Exam)
            .options(
                selectinload(Exam.official_notifications)
                    .selectinload(OfficialNotification.rule_groups)
                    .selectinload(EligibilityRuleGroup.rules)
                    .selectinload(EligibilityRule.attribute)
                            )
            .where(
                Exam.exam_id == exam_id
            )
        )

        if exam is None:
            raise ValueError("Exam not found")

        notifications = exam.official_notifications

        if not notifications:
            raise ValueError("No official notifications found")

        notification = max(
            notifications,
            key=lambda n: n.release_date
        )

        return notification.rule_groups
       
def check_rule(student, rule):
    attribute = rule.attribute.attribute_name.lower()

    if attribute in [
        "nationality",
        "state",
        "gender"
    ]:
        student_value = get_student_value(
            student,
            attribute
        )

    elif attribute in [
        "cgpa",
        "percentage",
        "qualification",
        "specialization",
        "current_year",
        "year_of_passing"
    ]:
        student_value = get_education_value(
            student,
            attribute
        )

    else:
        raise ValueError(
            f"Unsupported attribute: {attribute}"
        )
    rule_value = rule.value

    if rule.attribute.data_type == "numeric":
        rule_value = float(rule_value)

    elif rule.attribute.data_type == "date":
        pass

    return evaluate_rule(
        student_value,
        rule.operator,
        rule_value
    )
def check_rule_group(student, group):

    results = []

    for rule in group.rules:
        results.append(
            check_rule(student, rule)
        )

    if not results:
        return True

    if group.logical_operator == "AND":
        return all(results)

    elif group.logical_operator == "OR":
        return any(results)

    else:
        raise ValueError(
            f"Unsupported logical operator: {group.logical_operator}"
        )        
def check_eligibility(student, exam_id):

    groups = get_exam_rule_groups(exam_id)

    for group in groups:

        if not check_rule_group(student, group):
            return False

    return True
