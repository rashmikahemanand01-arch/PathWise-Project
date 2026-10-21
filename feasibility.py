
from datetime import date
from math import ceil

from projects import PROJECTS


def evaluate_project(project, student):
    # 1. Calculate the time available before the deadline.
    days_left = (student["deadline"] - date.today()).days

    available_hours = (
        student["hours_per_week"] * days_left / 7
    )

    # 2. Estimate the complete project workload.
    learning_hours = project["learning_hours"]
    build_hours = project["build_hours"]

    # Testing and deployment are included in the total estimate.
    testing_hours = max(2, ceil(build_hours * 0.15))
    deployment_hours = max(1, ceil(build_hours * 0.10))

    required_hours = (
        learning_hours
        + build_hours
        + testing_hours
        + deployment_hours
    )

    # 3. Match skills without being affected by capitalization.
    student_skills = {
        skill.strip().lower()
        for skill in student["skills"]
    }

    required_skills = project["required_skills"]

    missing_skills = [
        skill
        for skill in required_skills
        if skill.strip().lower() not in student_skills
    ]

    if required_skills:
        matched_count = len(required_skills) - len(missing_skills)
        skill_match = matched_count / len(required_skills)
    else:
        skill_match = 1.0

    # 4. Calculate time fit.
    if required_hours > 0:
        time_ratio = available_hours / required_hours
    else:
        time_ratio = 1.0

    if time_ratio >= 1.5:
        time_score = 35
    elif time_ratio >= 1.15:
        time_score = 30
    elif time_ratio >= 1.0:
        time_score = 25
    elif time_ratio >= 0.75:
        time_score = 17
    elif time_ratio >= 0.5:
        time_score = 9
    else:
        time_score = 3

    # 5. Calculate budget fit.
    estimated_cost = project["cost"]
    enough_budget = student["budget"] >= estimated_cost

    if enough_budget:
        budget_score = 15
    else:
        budget_score = 0

    # 6. Score the project's skill requirements.
    skill_score = round(skill_match * 35)

    # 7. Account for project difficulty.
    difficulty = project["difficulty"].strip().lower()

    if difficulty == "beginner":
        difficulty_score = 15
    elif difficulty == "intermediate":
        difficulty_score = 11
    else:
        difficulty_score = 7

    # 8. Combine the scoring components.
    score = (
        skill_score
        + time_score
        + budget_score
        + difficulty_score
    )

    score = max(0, min(100, round(score)))

    # 9. Explain the result.
    enough_time = available_hours >= required_hours

    if not enough_budget or time_ratio < 0.5:
        status = "Unrealistic"
    elif enough_time and not missing_skills:
        status = "Feasible"
    else:
        status = "Tight"

    reasons = [
        (
            f"Effort breakdown: {learning_hours} learning, "
            f"{build_hours} building, {testing_hours} testing, "
            f"and {deployment_hours} deployment hours."
        ),
        (
            f"Total estimated effort: {required_hours} hours "
            f"compared with {available_hours:.1f} available hours."
        ),
    ]

    if missing_skills:
        reasons.append(
            "Skills to learn first: "
            + ", ".join(missing_skills)
            + "."
        )
    else:
        reasons.append(
            "Your listed skills cover the project's prerequisites."
        )

    if time_ratio < 1:
        reasons.append(
            "The full project may not fit your deadline. "
            "Use the smaller-scope alternative or allow more time."
        )
    elif time_ratio < 1.25:
        reasons.append(
            "Your schedule has limited flexibility for unexpected problems."
        )
    else:
        reasons.append(
            "Your time estimate includes some room for revisions."
        )

    if not enough_budget:
        reasons.append(
            f"The listed estimated cost is ₹{estimated_cost:.0f}, "
            "which exceeds your budget."
        )
    else:
        reasons.append(
            f"The listed estimated cost of ₹{estimated_cost:.0f} "
            "fits your budget, assuming the listed tools are sufficient."
        )

    if difficulty == "advanced":
        reasons.append(
            "This project has advanced requirements. Build a small "
            "working version before adding optional features."
        )
    elif difficulty == "intermediate":
        reasons.append(
            "Build the core workflow first, then add improvements "
            "after the main feature works."
        )
    else:
        reasons.append(
            "Start with the core feature and verify it works "
            "before polishing the interface."
        )

    return {
        "project": project,
        "score": score,
        "status": status,
        "required_hours": required_hours,
        "available_hours": round(available_hours, 1),
        "missing_skills": missing_skills,
        "reasons": reasons,
        "skill_match": round(skill_match * 100),
        "learning_hours": learning_hours,
        "build_hours": build_hours,
        "testing_hours": testing_hours,
        "deployment_hours": deployment_hours,
        "time_ratio": round(time_ratio, 2),
    }


def recommend_projects(student):
    results = []

    selected_category = student["category"]

    for project in PROJECTS:
        if (
            selected_category != "Any"
            and project["category"] not in (selected_category, "Any")
        ):
            continue

        results.append(evaluate_project(project, student))

    results.sort(
        key=lambda result: (
            result["status"] == "Feasible",
            result["score"],
            -len(result["missing_skills"]),
            -result["required_hours"],
        ),
        reverse=True,
    )

    return results[:20]

