def extract_exam_name(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    candidates = []

    for index, line in enumerate(lines[:40]):

        lower = line.lower()

        if len(line) < 5 or len(line) > 150:
            continue

        score = 0

        if "examination" in lower:
            score += 4

        elif "exam" in lower:
            score += 3

        if any(char.isdigit() for char in line):
            score += 1

        if line.isupper():
            score += 2

        if index < 10:
            score += 2

        if any(
            word in lower
            for word in [
                "commission",
                "department",
                "university",
                "government"
            ]
        ):
            score -= 2

        candidates.append((score, line))

    if not candidates:
        return None

    candidates.sort(
        key=lambda candidate: candidate[0],
        reverse=True
    )

    return candidates[0][1]