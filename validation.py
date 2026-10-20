
from datetime import date


def validate_project_inputs(form):
    errors = []

    category = form.get("category", "").strip()
    skills = form.getlist("skills")
    deadline_text = form.get("deadline", "").strip()
    hours_text = form.get("hours", "").strip()
    budget_text = form.get("budget", "").strip()

    allowed_categories = {"AI", "Web", "App", "Data", "Any"}

    allowed_skills = {
        "Python", "C", "C++", "Java", "JavaScript",
        "TypeScript", "HTML", "CSS", "SQL", "Flask",
        "Streamlit", "Django", "React", "Node.js",
        "Pandas", "NumPy", "Scikit-learn", "TensorFlow",
        "OpenCV", "NLP", "APIs", "Git", "File Handling",
        "Excel", "SQLite", "Firebase", "JSON", "Requests"
    }

    if category not in allowed_categories:
        errors.append("Please select a valid project category.")

    skills = [
        skill.strip()
        for skill in skills
        if skill.strip() in allowed_skills
    ]

    if not skills:
        skills = []

    hours = None
    budget = None
    deadline = None

    try:
        hours = int(hours_text)
        if not 1 <= hours <= 80:
            errors.append(
                "Available hours must be between 1 and 80 per week."
            )
    except ValueError:
        errors.append("Enter a valid number of hours per week.")

    try:
        budget = float(budget_text)
        if budget < 0:
            errors.append("Budget cannot be negative.")
    except ValueError:
        errors.append("Enter a valid project budget.")

    try:
        deadline = date.fromisoformat(deadline_text)
        if deadline <= date.today():
            errors.append("Choose a future deadline.")
    except ValueError:
        errors.append("Enter a valid deadline.")

    if errors:
        return None, errors

    data = {
        "category": category,
        "skills": [skill.lower() for skill in skills],
        "hours_per_week": hours,
        "budget": budget,
        "deadline": deadline,
    }

    return data, []

 

