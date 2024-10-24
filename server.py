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
    return jsonify(project_list)

@app.route("/generate", methods=["GET"])
def generate():
    return render_template("generate.html") 

@app.route("/generate", methods=["POST"])
def generate_report():
    projectName = request.form.get("projectName")
    reporterName = request.form.get("reporterName")
    startDate = request.form.get("startDate")
    endDate = request.form.get("endDate")
    executiveSummary = request.form.get("executiveSummary")
    vulnCount = int(request.form.get("vulnCount"))
    vulnerabilities = []
    last_project = db.session.query(Project).order_by(Project.project_id.desc()).first()
    if last_project:
        project_id = last_project.project_id+1
    else:
        project_id = 1

    for i in range(1, vulnCount+1):
        vulnerability = {
            "vulnerability_name": request.form.get(f"vulnerabilityTitle-{i}"),
            "vulnerable_component": request.form.get(f"vulnerable_component-{i}"),
            "severity": request.form.get(f"severity-{i}"),
            "description": request.form.get(f"description-{i}"),
            "impact": request.form.get(f"impact-{i}"),
            "remediation": request.form.get(f"remediation-{i}"),
            "poc": "{{7*7}}"
        }
        vulnerabilities.append(vulnerability)
        
        new_vulnerability_obj = Vulnerability(
            project_id = project_id,
            title = vulnerability["vulnerability_name"],
            severity = vulnerability["severity"],
            vulnerable_component = vulnerability["vulnerable_component"],
            description = vulnerability["description"],
            impact = vulnerability["impact"],
            remediation = vulnerability["remediation"],
            poc = vulnerability["poc"]
        )
        db.session.add(new_vulnerability_obj)
        db.session.commit()
    
    new_project = Project(
        project_name=projectName,
        reporter_name=reporterName,
        start_date=startDate,
        end_date=endDate,
        executive_summary=executiveSummary,
        vuln_count=vulnCount
    )

    db.session.add(new_project)
    db.session.commit()

    generate_pentest_report(projectName, startDate, reporterName, vulnerabilities, "logo.png", executiveSummary, f"reports/report-{new_project.project_id}.docx")

    return redirect("/")

@app.route("/delete", methods=["GET"])
def delete():
    project_id = int(request.args.get("project_id"))
    Project.query.filter_by(project_id=project_id).delete()
    db.session.commit()
    return redirect("/")

@app.route("/edit", methods=["GET"])
def get_edit():
    project_id = int(request.args.get("project_id"))
    project = Project.query.get_or_404(project_id)
    vulnerabilities = Vulnerability.query.filter(project_id == project_id).all()
    return render_template("edit.html", project=project, vulnerabilities=vulnerabilities)

@app.route("/edit", methods=["POST"])
def post_edit():
    print(request.form)
    project_id = int(request.form.get("project_id"))
    project = Project.query.get_or_404(project_id)
    vulnCount = project.vuln_count

    project.project_name = request.form.get("project_name")
    project.reporter_name = request.form.get("reporter_name")
    project.start_date = request.form.get("start_date")
    project.end_date = request.form.get("end_date")
    project.executive_summary = request.form.get("executive_summary")
    db.session.commit()

    # remove old vulnerability entries
    delete_q = Vulnerability.__table__.delete().where(Vulnerability.project_id == project_id)
    db.session.execute(delete_q)
    db.session.commit()
    print(vulnCount)
    print(request.form.get(f"vulnerable_component-1"))

    # insert new ones
    columns = ["vulnerabilityTitle", "vulnerable_component" "description", "remediation", "impact", "poc"]
    for i in range(1, vulnCount+1):
        print(request.form.get(f"vulnerable_component-{i}"))
        new_vulnerability_obj = Vulnerability(
            project_id = project_id,
            title = request.form.get(f"vulnerabilityTitle-{i}"),
            severity = request.form.get(f"severity-{i}"),
            vulnerable_component = request.form.get(f"vulnerable_component-{i}"),
            description = request.form.get(f"description-{i}"),
            impact = request.form.get(f"impact-{i}"),
            remediation = request.form.get(f"remediation-{i}"),
            poc = request.form.get(f"poc-{i}"),
        )
        db.session.add(new_vulnerability_obj)
        db.session.commit()

    return render_template("index.html", message="Project edited successfully")

@app.route("/download", methods=["GET"])
def download():
    project_id = int(request.args.get("project_id"))
    return send_file(f"reports/report-{project_id}.docx")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)