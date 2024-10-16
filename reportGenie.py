from docx import Document
from docx.shared import RGBColor


def generate_pentest_report(report_title, start_date, end_date, reporter_name, vulnerabilities):
    # Load the report template
    template_path = 'report.docx'  # Replace with your actual template path
    doc = Document(template_path)

    # Replace placeholders with input values, preserving formatting
    for paragraph in doc.paragraphs:
        if '{REPORT_TITLE}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{REPORT_TITLE}', report_title)
        if '{START_DATE}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{START_DATE}', start_date)
        if '{END_DATE}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{END_DATE}', end_date)
        if '{REPORTER_NAME}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{REPORTER_NAME}', reporter_name)

    # Add vulnerabilities to the report
    for i, vuln in enumerate(vulnerabilities, start=1):
        # Add vulnerability name as a heading (Heading 2)
        heading = doc.add_heading(level=2)
        heading_run = heading.add_run(f"{i}. {vuln['vulnerability_name']}")

        # Add severity with specific color formatting
        severity_paragraph = doc.add_paragraph()
        severity_run = severity_paragraph.add_run(f"Severity: {vuln['severity']}")
        severity_run.bold = True
        if vuln['severity'].lower() == 'critical':
            severity_run.font.color.rgb = RGBColor(128, 0, 0)  # Burgundy
        elif vuln['severity'].lower() == 'high':
            severity_run.font.color.rgb = RGBColor(255, 0, 0)  # Red
        elif vuln['severity'].lower() == 'medium':
            severity_run.font.color.rgb = RGBColor(255, 165, 0)  # Orange
        elif vuln['severity'].lower() == 'low':
            severity_run.font.color.rgb = RGBColor(0, 0, 255)  # Blue
        elif vuln['severity'].lower() == 'informational':
            severity_run.font.color.rgb = RGBColor(0, 128, 0)  # Green
        else:
            severity_run.font.color.rgb = RGBColor(0, 0, 0)  # Black

        # Add vulnerable component
        vulnerable_component_paragraph = doc.add_paragraph()
        vulnerable_component_run = vulnerable_component_paragraph.add_run(f"URL/Vulnerable component: {vuln['vulnerable_component']}")
        vulnerable_component_run.bold = True

        # Add description
        description_paragraph = doc.add_paragraph()
        description_run = description_paragraph.add_run(f"Description: {vuln['description']}")
        description_run.bold = True

        # Add impact
        impact_paragraph = doc.add_paragraph()
        impact_run = impact_paragraph.add_run(f"Impact: {vuln['impact']}")
        impact_run.bold = True

        # Add remediation
        remediation_paragraph = doc.add_paragraph()
        remediation_run = remediation_paragraph.add_run(f"Remediation: {vuln['remediation']}")
        remediation_run.bold = True

        # Add PoC
        poc_paragraph = doc.add_paragraph()
        poc_run = poc_paragraph.add_run(f"PoC: {vuln['poc']}")
        poc_run.bold = True

    # Save the document to a new file
    output_path = 'pentest_report_output.docx'
    doc.save(output_path)
    print(f"Report generated: {output_path}")

# Example usage
vulnerabilities = [
    {
        'vulnerability_name': 'SQL Injection',
        'vulnerable_component': 'http://example.com/login',
        'severity': 'High',
        'description': 'SQL injection vulnerability in login form.',
        'impact': 'Access to all user data.',
        'remediation': 'Use parameterized queries.',
        'poc': 'Use this bypass authentication.'
    },
    {
        'vulnerability_name': 'Cross-Site Scripting',
        'vulnerable_component': 'http://example.com/comment',
        'severity': 'Medium',
        'description': 'Reflected XSS in comment section.',
        'impact': 'Stealing session cookies.',
        'remediation': 'Sanitize user input.',
        'poc': '<script>alert("XSS")</script>'
    }
]

generate_pentest_report('Sample Pentest Report', '2024-01-01', '2024-01-31', 'John Doe', vulnerabilities)