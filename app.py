from flask import Flask, render_template, request
from validation import validate_project_inputs
from feasibility import recommend_projects

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/form")
def project_form():
    return render_template("form.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    student, errors = validate_project_inputs(request.form)

    if errors:
        return render_template("form.html", errors=errors), 400

    results = recommend_projects(student)

    return render_template(
        "results.html",
        results=results,
        student=student
    )


if __name__ == "__main__":
    app.run(debug=True)
