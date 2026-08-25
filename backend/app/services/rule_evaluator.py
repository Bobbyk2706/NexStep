def evaluate_rule(student_value, operator, rule_value):

    if operator == "=":
        return student_value == rule_value

    elif operator == "!=":
        return student_value != rule_value

    elif operator == ">":
        return student_value > rule_value

    elif operator == ">=":
        return student_value >= rule_value

    elif operator == "<":
        return student_value < rule_value

    elif operator == "<=":
        return student_value <= rule_value

    else:
        raise ValueError(f"Unsupported operator: {operator}")