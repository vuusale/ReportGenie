from flask import Flask, request, send_file, render_template, redirect, jsonify
from base64 import b64encode, b64decode
from urllib.parse import quote_plus, unquote_plus
from reportGenie import generate_pentest_report
from app import app, db, Project, Vulnerability

app.jinja_env.filters["quote_plus"] = lambda u: quote_plus(u)
app.jinja_env.filters["b64encode"] = lambda u: b64encode(u.encode()).decode()
app.jinja_env.filters["b64decode"] = lambda u: b64decode(u.encode()).decode()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", message="Salam") 

@app.route("/projects", methods=["GET"])
def projects():
    projects = Project.query.all()
    project_list = []
    for project in projects:
        project_data = {
            'project_id': project.project_id,
            'project_name': project.project_name,
            'reporter_name': project.reporter_name,
            'start_date': project.start_date,
            'end_date': project.end_date,
            'executive_summary': project.executive_summary,
            'vulnerabilities': [vuln.vulnerability_id for vuln in project.vulnerabilities]
        }
        project_list.append(project_data)
    print(project_list)
    return jsonify(project_list)

@app.route("/generate", methods=["GET"])
def generate():
    return render_template("generate.html") 

@app.route("/generate", methods=["POST"])
def generate_report():
    projectName = request.form.get("projectName")
    reporterName = request.form.get("reporterName")
    testDate = request.form.get("testDate")
    vulnCount = int(request.form.get("vulnCount"))
    vulnerabilities = []
    for i in range(1, vulnCount+1):
        vulnerability = {
        "vulnerability_name": request.form.get(f"vulnerabilityTitle-{i}"),
        "vulnerable_component": "http://example.com/comment",
        "severity": request.form.get(f"severity-{i}"),
        "description": request.form.get(f"description-{i}"),
        "impact": request.form.get(f"impact-{i}"),
        "remediation": request.form.get(f"remediation-{i}"),
        "poc": "{{7*7}}"
        }
        vulnerabilities.append(vulnerability)
    
    generate_pentest_report(projectName, testDate, reporterName, vulnerabilities, "logo.png", "executive_summary")
    new_project = Project(
        project_name=projectName,
        reporter_name=reporterName,
        start_date=testDate,
        end_date=testDate,
        executive_summary="d"
    )
    db.session.add(new_project)
    db.session.commit()

    return render_template("index.html", message="Report ready for download")

@app.route("/delete", methods=["GET"])
def delete():
    project_id = int(request.args.get("project_id"))
    Project.query.filter_by(project_id=project_id).delete()
    db.session.commit()
    return render_template("index.html", message=f"Project deleted successfully")

@app.route("/edit", methods=["GET"])
def get_edit():
    project_id = int(request.args.get("project_id"))
    project = Project.query.get_or_404(project_id)
    return render_template("edit.html", project=project)

@app.route("/edit", methods=["POST"])
def post_edit():
    project_id = int(request.form.get("project_id"))
    project = Project.query.get_or_404(project_id)

    project.project_name = request.form.projectName
    project.reporter_name = request.form.reporterName
    project.start_date = request.form.testDate
    project.end_date = request.form.testDate
    project.executive_summary = "request.form.executive_summary"

    db.session.commit()

    return render_template("index.html", message="Project edited successfully")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)