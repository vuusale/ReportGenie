from flask import request, send_file, render_template, redirect, jsonify
from base64 import b64encode, b64decode
from urllib.parse import quote_plus
from reportGenie import generate_pentest_report
from app import app, db, Project, Vulnerability
import json

app.jinja_env.filters["quote_plus"] = lambda u: quote_plus(u)
app.jinja_env.filters["b64encode"] = lambda u: b64encode(u.encode()).decode()
app.jinja_env.filters["b64decode"] = lambda u: b64decode(u.encode()).decode()
columns = ["vulnerability_name", "severity", "vulnerable_component", "description", "remediation", "impact", "poc"]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", message="Salam") 

@app.route("/projects", methods=["GET"])
def projects():
    projects = Project.query.all()
    project_list = []
    for project in projects:
        vulnerabilities = Vulnerability.query.filter(Vulnerability.project_id == project.project_id).all()
        project_data = {
            'project_id': project.project_id,
            'project_name': project.project_name,
            'start_date': project.start_date,
            'vuln_count': len(vulnerabilities)
        }
        project_list.append(project_data)
    return jsonify(project_list)

@app.route("/generate", methods=["GET"])
def generate():
    with open('settings.json') as f:
        settings = json.load(f)
    return render_template("generate.html", settings=settings) 

@app.route("/generate", methods=["POST"])
def generate_report():
    project_name = request.form.get("project_name")
    reporter_name = request.form.get("reporter_name")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    executive_summary = request.form.get("executive_summary")
    vuln_count = int(request.form.get("vuln_count"))
    vulnerabilities = []
    last_project = db.session.query(Project).order_by(Project.project_id.desc()).first()
    if last_project:
        project_id = last_project.project_id+1
    else:
        project_id = 1

    for i in range(1, vuln_count+1):
        vulnerability = {}
        for column in columns:
            vulnerability[column] = request.form.get(f"{column}-{i}")
        vulnerabilities.append(vulnerability)
        new_vulnerability_obj = Vulnerability(
            project_id = project_id,
            **vulnerability
        )
        db.session.add(new_vulnerability_obj)
        db.session.commit()
    
    new_project = Project(
        project_name=project_name,
        reporter_name=reporter_name,
        start_date=start_date,
        end_date=end_date,
        executive_summary=executive_summary,
        vuln_count=vuln_count
    )

    db.session.add(new_project)
    db.session.commit()

    with open("settings.json", "rb") as f:
        settings = json.load(f)

    generate_pentest_report(project_name, start_date, reporter_name, vulnerabilities, settings["icon_path"], executive_summary, f"reports/report-{new_project.project_id}.docx")

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
    vulnerabilities = Vulnerability.query.filter(Vulnerability.project_id == project_id).all()
    return render_template("edit.html", project=project, vulnerabilities=vulnerabilities)

@app.route("/edit", methods=["POST"])
def post_edit():
    project_id = int(request.form.get("project_id"))
    vuln_count = int(request.form.get("vuln_count"))
    project = Project.query.get_or_404(project_id)

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

    # insert new ones
    for i in range(1, vuln_count+1):
        vulnerability = {}
        for column in columns:
            vulnerability[f"{column}"] = request.form.get(f"{column}-{i}")
        new_vulnerability_obj = Vulnerability(
            project_id = project_id,
            **vulnerability
        )
        db.session.add(new_vulnerability_obj)
        db.session.commit()

    return render_template("index.html", message="Project edited successfully")

@app.route("/download", methods=["GET"])
def download():
    project_id = int(request.args.get("project_id"))
    project = Project.query.get_or_404(Project.project_id == project_id)
    generate_pentest_report(project.project_name, project.start_date, project.reporter_name, project.vulnerabilities, settings.icon_path, project.executive_summary, f"reports/report-{project_id}.docx")

    return send_file(f"reports/report-{project_id}.docx")

@app.route("/settings", methods=["GET"])
def get_settings():
    with open("settings.json", "rb") as f:
        settings = json.load(f)
    return render_template("settings.html", settings=settings)

@app.route("/settings", methods=["POST"])
def post_settings():
    with open("settings.json", "rb") as f:
        settings = json.load(f)
    return render_template("settings.html", settings=settings)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)