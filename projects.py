def estimate_project_cost(category, skills):
    """
    Estimate optional hosting and external-service costs.
    These are planning allowances, not guaranteed prices.
    A local prototype may cost ₹0.
    """
    skill_names = {skill.strip().lower() for skill in skills}

    category_allowance = {
        "AI": 200,
        "Web": 150,
        "App": 150,
        "Data": 50,
        "Any": 0,
    }

    estimated_cost = category_allowance.get(category, 0)

    if "apis" in skill_names:
        estimated_cost += 300

    if "firebase" in skill_names:
        estimated_cost += 300

    return estimated_cost


def make_project(
    project_id,
    name,
    category,
    skills,
    learning,
    build,
    difficulty,
    description,
    reduced_scope,
    cost=None,
):
    if cost is None:
        cost = estimate_project_cost(category, skills)

    return {
        "id": project_id,
        "name": name,
        "category": category,
        "required_skills": skills,
        "learning_hours": learning,
        "build_hours": build,
        "cost": cost,
        "cost_note": (
            "Planning estimate for optional hosting or external services. "
            "A local prototype may cost ₹0. Verify current free-tier limits "
            "and provider pricing before deployment."
        ),
        "difficulty": difficulty,
        "description": description,
        "reduced_scope": reduced_scope,
    }


PROJECTS = [                 "Create a batch pipeline with an execution log."),
    make_project("data14", "Climate Pattern Explorer", "Data",
                 ["Python", "Pandas", "Matplotlib"], 16, 28, "Intermediate",
                 "Explore temperature and rainfall patterns using public records.",
                 "Analyze one location's historical data."),
    make_project("data15", "Housing Data Analysis", "Data",
                 ["Python", "Pandas", "Scikit-learn"], 18, 30, "Advanced",
                 "Explore housing features and evaluate baseline price models.",
                 "Use a public dataset and a baseline regression."),
    make_project("data16", "Election Data Visualization", "Data",
                 ["Python", "Pandas", "Matplotlib"], 16, 28, "Intermediate",
                 "Visualize published election statistics with clear source attribution.",
                 "Analyze one published dataset without predicting outcomes."),
    make_project("data17", "Job Market Skills Analyzer", "Data",
                 ["Python", "Pandas", "SQL"], 16, 28, "Intermediate",
                 "Summarize in-demand skills from a curated set of job postings.",
                 "Analyze a legally obtained sample dataset."),
    make_project("data18", "Web Traffic Analytics Dashboard", "Data",
                 ["Python", "Pandas", "Matplotlib"], 16, 28, "Intermediate",
                 "Analyze visits, referral sources, and engagement in sample web data.",
                 "Create a dashboard from sample traffic logs."),
    make_project("data19", "Supply Chain Performance Dashboard", "Data",
                 ["Python", "Pandas", "SQL", "Matplotlib"], 18, 30, "Advanced",
                 "Analyze lead times, stockouts, and delivery performance.",
                 "Use sample supply-chain records."),
    make_project("data20", "Dataset Search and Catalog", "Data",
                 ["Python", "Pandas", "SQL"], 14, 26, "Intermediate",
                 "Index dataset metadata and make it searchable by topic and format.",
                 "Catalog local CSV files and their column names."),

    # ========== 5. AUTOMATION & CROSS-DOMAIN (20) ==========
    make_project("auto01", "Intelligent File Organizer", "Any",
                 ["Python", "File Handling"], 6, 14, "Beginner",
                 "Organize files by type and configurable rules.",
                 "Preview proposed moves before applying them."),
    make_project("auto02", "Automated Spreadsheet Reporting", "Any",
                 ["Python", "Pandas", "Excel"], 10, 20, "Intermediate",
                 "Clean recurring spreadsheets and generate reports.",
                 "Process one workbook and export a summary."),
    make_project("auto03", "Website Change Monitor", "Any",
                 ["Python", "Requests", "HTML"], 12, 22, "Intermediate",
                 "Record changes on selected public webpages.",
                 "Monitor one permitted webpage."),
    make_project("auto04", "Deadline and Application Tracker", "Any",
                 ["Python", "Flask", "SQL"], 12, 22, "Intermediate",
                 "Organize application deadlines, priorities, and statuses.",
                 "Build a searchable tracker."),
    make_project("auto05", "Document Batch Processing Toolkit", "Any",
                 ["Python", "File Handling"], 10, 20, "Intermediate",
                 "Batch-process supported documents and index metadata.",
                 "Process PDFs and text files."),
    make_project("auto06", "Dataset Update Pipeline", "Any",
                 ["Python", "Pandas", "SQL"], 16, 28, "Advanced",
                 "Validate data updates and log rejected records.",
                 "Load CSVs and validate required columns."),
    make_project("auto07", "Public API Status Dashboard", "Any",
                 ["Python", "APIs", "Flask"], 14, 24, "Intermediate",
                 "Combine public API information into one dashboard.",
                 "Integrate one public API."),
    make_project("auto08", "Local Document Search Engine", "Any",
                 ["Python", "SQL", "File Handling"], 16, 28, "Advanced",
                 "Index local documents and retrieve matching content.",
                 "Search filenames and extracted text."),
    make_project("auto09", "Email Attachment Sorting Assistant", "Any",
                 ["Python", "File Handling"], 10, 20, "Intermediate",
                 "Organize user-provided email attachments by type and project.",
                 "Sort downloaded files without connecting to email accounts."),
    make_project("auto10", "Duplicate File Detection Tool", "Any",
                 ["Python", "File Handling"], 8, 16, "Beginner",
                 "Identify duplicate files using file hashes.",
                 "Generate a report without deleting files."),
    make_project("auto11", "Automated PDF Report Generator", "Any",
                 ["Python", "Pandas"], 12, 22, "Intermediate",
                 "Generate consistent PDF reports from structured data.",
                 "Create one report template from a CSV."),
    make_project("auto12", "Folder Backup Verification Tool", "Any",
                 ["Python", "File Handling"], 10, 20, "Intermediate",
                 "Compare folders and report missing or changed files.",
                 "Compare file names, sizes, and hashes."),
    make_project("auto13", "CSV-to-Database Import Assistant", "Any",
                 ["Python", "Pandas", "SQL"], 12, 22, "Intermediate",
                 "Import CSV records with schema checks and error logs.",
                 "Load one CSV into a local SQLite database."),
    make_project("auto14", "Scheduled Data Collection Prototype", "Any",
                 ["Python", "Requests", "APIs"], 14, 24, "Intermediate",
                 "Collect permitted public data and record collection history.",
                 "Run a manually triggered collection script."),
    make_project("auto15", "File Naming Convention Validator", "Any",
                 ["Python", "File Handling"], 6, 14, "Beginner",
                 "Check files against configurable naming rules.",
                 "Report files that violate a naming pattern."),
    make_project("auto16", "Personal Workflow Automation Dashboard", "Any",
                 ["Python", "Flask", "SQL"], 16, 28, "Advanced",
                 "Organize repeatable workflows, task states, and execution logs.",
                 "Create a dashboard for three predefined workflows."),
    make_project("auto17", "Form Response Processing Pipeline", "Any",
                 ["Python", "Pandas", "SQL"], 12, 22, "Intermediate",
                 "Validate form exports and summarize submitted responses.",
                 "Clean a CSV and generate aggregate results."),
    make_project("auto18", "Broken Link Reporting Tool", "Any",
                 ["Python", "Requests", "HTML"], 12, 22, "Intermediate",
                 "Check links on permitted webpages and create a report.",
                 "Check links from one provided webpage."),
    make_project("auto19", "Local Inventory Import Automation", "Any",
                 ["Python", "Pandas", "SQL"], 12, 22, "Intermediate",
                 "Import inventory files and flag inconsistent stock records.",
                 "Validate one CSV and export exceptions."),
    make_project("auto20", "Personal Knowledge Backup Tool", "Any",
                 ["Python", "File Handling", "SQL"], 14, 24, "Intermediate",
                 "Export selected notes and metadata into a structured backup.",
                 "Back up one local notes folder and verify file counts."),
]
