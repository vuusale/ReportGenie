from flask import Flask, request, send_file, render_template, redirect
from base64 import b64encode, b64decode
from urllib.parse import quote_plus, unquote_plus
from reportGenie import generate_pentest_report
from threading import Thread

app = Flask(__name__, static_url_path='', static_folder='templates/static', template_folder='templates')
database = r"sqlite.db"
app.jinja_env.filters['quote_plus'] = lambda u: quote_plus(u)
app.jinja_env.filters['b64encode'] = lambda u: b64encode(u.encode()).decode()
app.jinja_env.filters['b64decode'] = lambda u: b64decode(u.encode()).decode()

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html") 

@app.route("/generate", methods=['GET'])
def generate():
    return render_template("generate.html") 

@app.route("/projects", methods=['GET'])
def projects():
    return [{
        "name": "Mobile application",
        "date": "2024-11-08",
        "status": "Active"
    }]

@app.route("/generate", methods=['POST'])
def generate_report():
    projectName = request.form.get('projectName')
    reporterName = request.form.get('reporterName')
    testDate = request.form.get('testDate')
    vulnCount = int(request.form.get('vulnCount'))
    vulnerabilities = []
    for i in range(1, vulnCount+1):
        vulnerability = {
        'vulnerability_name': request.form.get(f"vulnerabilityTitle-{i}"),
        'vulnerable_component': 'http://example.com/comment',
        'severity': request.form.get(f"severity-{i}"),
        'description': request.form.get(f"description-{i}"),
        'impact': request.form.get(f"impact-{i}"),
        'remediation': request.form.get(f"remediation-{i}"),
        'poc': '{{7*7}}'
        }
        vulnerabilities.append(vulnerability)
    
    generate_pentest_report(projectName, testDate, reporterName, vulnerabilities, "logo.png", "executive_summary")

    return send_file("pentest_report_output.docx")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000)