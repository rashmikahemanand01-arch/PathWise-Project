
from datetime import date
from math import ceil

from projects import PROJECTS


def evaluate_project(project, student):
    # 1. Calculate the time available before the deadline.
    days_left = max(
        0, (student["deadline"] - date.today()).days
    )

    available_hours = (
        student["hours_per_week"] * days_left / 7
    )

    # 2. Match skills before estimating personalized learning effort.
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

    # 3. Estimate effort for this project and this student.
    base_learning_hours = project["learning_hours"]
    learning_bonus = min(len(missing_skills) * 2, 12)

    learning_hours = base_learning_hours + learning_bonus
    build_hours = project["build_hours"]

    testing_hours = max(2, ceil(build_hours * 0.15))
    deployment_hours = max(1, ceil(build_hours * 0.10))

    required_hours = (
        learning_hours
        + build_hours
        + testing_hours
        + deployment_hours
    )

    # 4. Calculate time fit continuously, not in broad score bands.
    time_ratio = (
        available_hours / required_hours
        if required_hours > 0
        else 1.5
    )

    time_score = round(
        35 * min(max(time_ratio, 0), 1.5) / 1.5
    )

    # 5. Calculate budget fit.
    estimated_cost = float(project.get("cost", 0))
    budget = float(student["budget"])

    enough_budget = budget >= estimated_cost

    if estimated_cost <= 0:
        budget_score = 15
    else:
        budget_score = round(
            15 * min(max(budget / estimated_cost, 0), 1)
        )

    # 6. Calculate skill and difficulty fit.
    skill_score = round(skill_match * 35)

    difficulty = project["difficulty"].strip().lower()

    if difficulty == "beginner":
        difficulty_score = 15
    elif difficulty == "intermediate":
        difficulty_score = 11
    else:
        difficulty_score = 7

    # 7. Calculate the overall fit score.
    score = max(
        0,
        min(
            100,
            skill_score
            + time_score
            + budget_score
            + difficulty_score,
        ),
    )

    # 8. Determine feasibility.
    enough_time = available_hours >= required_hours

    if not enough_budget or time_ratio < 0.5:
        status = "Unrealistic"
    elif enough_time and not missing_skills:
        status = "Feasible"
    else:
        status = "Tight"

    # 9. Explain the recommendation.
    reasons = [
        (
            f"Effort breakdown: {learning_hours} learning, "
            f"{build_hours} building, {testing_hours} testing, "
            f"and {deployment_hours} deployment hours."
        ),
        (
            f"Total estimated effort: {required_hours} hours; "
            f"available time: {available_hours:.1f} hours."
        ),
        (
            f"Your current skills match "
            f"{round(skill_match * 100)}% of the listed prerequisites."
        ),
    ]

    if missing_skills:
        reasons.append(
            "Skills to learn: " + ", ".join(missing_skills) + "."
        )
    else:
        reasons.append(
            "Your listed skills cover the project's prerequisites."
        )

    if time_ratio < 1:
        reasons.append(
            "The estimated workload exceeds your available time. "
            "Consider reducing the project scope."
        )
    elif time_ratio < 1.25:
        reasons.append(
            "Your schedule has limited flexibility for unexpected issues."
        )
    else:
        reasons.append(
            "Your schedule has some room for revisions and debugging."
        )

    if not enough_budget:
        reasons.append(
            f"The estimated cost of ₹{estimated_cost:.0f} "
            f"exceeds your budget of ₹{budget:.0f}."
        )
    else:
        reasons.append(
            f"The estimated cost of ₹{estimated_cost:.0f} "
            "fits your budget. Verify actual service costs."
        )

    if difficulty == "advanced":
        reasons.append(
            "Build a small proof of concept before integrating "
            "all features."
        )
    elif difficulty == "intermediate":
        reasons.append(
            "Complete the core workflow before adding optional features."
        )
    else:
        reasons.append(
            "Start with the main feature and test it before polishing."
        )

    # 10. Identify risks.
    risks = []

    if missing_skills:
        risks.append(
            "Prerequisite gap: practise "
            + ", ".join(missing_skills[:3])
            + " before implementing the full project."
        )

    if time_ratio < 1:
        risks.append(
            "Deadline risk: the estimated workload exceeds "
            "your available hours. Reduce optional features."
        )
    elif time_ratio < 1.25:
        risks.append(
            "Schedule risk: reserve time for debugging and testing."
        )

    if difficulty == "advanced":
        risks.append(
            "Complexity risk: validate a small prototype first."
        )

    if not enough_budget:
        risks.append(
            "Budget risk: check whether free tools can replace "
            "paid services."
        )

    if not risks:
        risks.append(
            "Execution risk: unexpected bugs or integration problems. "
            "Test features as you build them."
        )

    # 11. Create project milestones.
    scope_hours = max(1, ceil(build_hours * 0.10))
    core_build_hours = max(1, build_hours - scope_hours)

    milestones = [
        {
            "title": "Define the project scope",
            "description": (
                "Choose essential features and decide what to exclude "
                "from the first version."
            ),
            "hours": scope_hours,
        },
        {
            "title": "Learn and prepare",
            "description": (
                "Review missing prerequisites and prepare "
                "the development environment."
            ),
            "hours": learning_hours,
        },
        {
            "title": "Build the core feature",
            "description": (
                "Implement the main workflow and test representative inputs."
            ),
            "hours": core_build_hours,
        },
        {
            "title": "Test and fix issues",
            "description": (
                "Check normal inputs, invalid inputs, and edge cases."
            ),
            "hours": testing_hours,
        },
        {
            "title": "Prepare the final version",
            "description": (
                "Deploy if applicable, review usability, "
                "and document limitations."
            ),
            "hours": deployment_hours,
        },
    ]

    # 12. Return all values used by results.html.
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
        "risks": risks,
        "milestones": milestones,
        "score_breakdown": {
            "Skill match": skill_score,
            "Time fit": time_score,
            "Budget fit": budget_score,
            "Difficulty fit": difficulty_score,
        },
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

        
        
             
    
