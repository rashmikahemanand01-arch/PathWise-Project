from datetime import date
from projects import PROJECTS


def evaluate_project(project, student):
    days_left = (student["deadline"] - date.today()).days
    available_hours = student["hours_per_week"] * days_left / 7

    required_hours = (
        project["learning_hours"] + project["build_hours"]
    )

    student_skills = set(student["skills"])
    required_skills = set(project["required_skills"])
    missing_skills = sorted(required_skills - student_skills)

    enough_time = available_hours >= required_hours
    enough_budget = student["budget"] >= project["cost"]

    score = 100

    if available_hours < required_hours:
        score -= 35

    if available_hours < required_hours * 1.25:
        score -= 10

    if not enough_budget:
        score -= 30

    score -= min(len(missing_skills) * 10, 30)
    score = max(0, score)

    if not enough_budget or available_hours < required_hours * 0.6:
        status = "Unrealistic"
    elif enough_time and enough_budget and len(missing_skills) <= 1:
        status = "Feasible"
    else:
        status = "Tight"

    reasons = [
        f"Estimated effort: {required_hours} hours.",
        f"Available time: {available_hours:.1f} hours."
    ]

    if missing_skills:
        reasons.append(
            "Skills to learn: " + ", ".join(missing_skills) + "."
        )
    else:
        reasons.append(
            "Your listed skills cover the project prerequisites."
        )

    if not enough_budget:
        reasons.append("The estimated cost exceeds your budget.")
    else:
        reasons.append("The estimated cost fits your budget.")

    if available_hours < required_hours:
        reasons.append(
            "Consider the reduced-scope version to lower the workload."
        )

    return {
        "project": project,
        "score": score,
        "status": status,
        "required_hours": required_hours,
        "available_hours": round(available_hours, 1),
        "missing_skills": missing_skills,
        "reasons": reasons,
    }


def recommend_projects(student):
    results = []

    for project in PROJECTS:
        if (
            student["category"] != "Any"
            and project["category"] != student["category"]
        ):
            continue

        results.append(evaluate_project(project, student))

    results.sort(
        key=lambda result: (
            result["status"] == "Feasible",
            result["score"]
        ),
        reverse=True
    )

    return results[:3]
