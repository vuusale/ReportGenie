from docx import Document
from docx.shared import RGBColor, Pt
from docx.enum.text import WD_LINE_SPACING
import matplotlib.pyplot as plt
import io
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches


def generate_pentest_report(report_title, date, reporter_name, vulnerabilities):
    # Load the report template
    template_path = 'report.docx'  # Replace with your actual template path
    doc = Document(template_path)

    # Replace placeholders with input values, preserving formatting
    for paragraph in doc.paragraphs:
        if '{REPORT_TITLE}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{REPORT_TITLE}', report_title)
        if '{DATE}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{DATE}', date)
        if '{REPORTER_NAME}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{REPORTER_NAME}', reporter_name)

    # Add vulnerabilities to the report
    for i, vuln in enumerate(vulnerabilities, start=1):
        # Add vulnerability name as a heading (Heading 2)
        heading = doc.add_heading(level=2)
        heading_run = heading.add_run(f"{i}. {vuln['vulnerability_name']}")

        # Set line spacing for vulnerabilities section
        heading.paragraph_format.line_spacing = 1.5

        # Add severity with specific color formatting
        severity_paragraph = doc.add_paragraph()
        severity_run = severity_paragraph.add_run("Severity: ")
        severity_run.bold = True
        severity_value_run = severity_paragraph.add_run(vuln['severity'])
        if vuln['severity'].lower() == 'critical':
            severity_value_run.font.color.rgb = RGBColor(128, 0, 0)  # Burgundy
        elif vuln['severity'].lower() == 'high':
            severity_value_run.font.color.rgb = RGBColor(255, 0, 0)  # Red
        elif vuln['severity'].lower() == 'medium':
            severity_value_run.font.color.rgb = RGBColor(255, 165, 0)  # Orange
        elif vuln['severity'].lower() == 'low':
            severity_value_run.font.color.rgb = RGBColor(0, 0, 255)  # Blue
        elif vuln['severity'].lower() == 'informational':
            severity_value_run.font.color.rgb = RGBColor(0, 128, 0)  # Green
        else:
            severity_value_run.font.color.rgb = RGBColor(0, 0, 0)  # Black

        severity_paragraph.paragraph_format.line_spacing = 1.5

        # Add vulnerable component
        vulnerable_component_paragraph = doc.add_paragraph()
        vulnerable_component_run = vulnerable_component_paragraph.add_run(f"URL/Vulnerable component: {vuln['vulnerable_component']}")
        vulnerable_component_run.bold = True
        vulnerable_component_paragraph.paragraph_format.line_spacing = 1.5

        # Add description
        description_paragraph = doc.add_paragraph()
        description_run = description_paragraph.add_run(f"Description: {vuln['description']}")
        description_run.bold = True
        description_paragraph.paragraph_format.line_spacing = 1.5

        # Add impact
        impact_paragraph = doc.add_paragraph()
        impact_run = impact_paragraph.add_run(f"Impact: {vuln['impact']}")
        impact_run.bold = True
        impact_paragraph.paragraph_format.line_spacing = 1.5

        # Add remediation
        remediation_paragraph = doc.add_paragraph()
        remediation_run = remediation_paragraph.add_run(f"Remediation: {vuln['remediation']}")
        remediation_run.bold = True
        remediation_paragraph.paragraph_format.line_spacing = 1.5

        # Add PoC
        poc_paragraph = doc.add_paragraph()
        poc_run = poc_paragraph.add_run(f"PoC: {vuln['poc']}")
        poc_run.bold = True
        poc_paragraph.paragraph_format.line_spacing = 1.5

    # Update the technical summary section with vulnerability statistics
    severity_counts = {
        'Critical': 0,
        'High': 0,
        'Medium': 0,
        'Low': 0,
        'Informational': 0,
        'Other': 0
    }
    
    for vuln in vulnerabilities:
        severity = vuln['severity'].capitalize()
        if severity in severity_counts:
            severity_counts[severity] += 1
        else:
            severity_counts['Other'] += 1

    # Replace the content of the technical summary table
    for table in doc.tables:
        if '{TECHNICAL_SUMMARY_TABLE}' in table.cell(0, 0).text:
            table.cell(0, 0).text = "Severity"
            table.cell(0, 1).text = "Count"
            row_idx = 1
            for severity, count in severity_counts.items():
                if row_idx < len(table.rows):
                    table.cell(row_idx, 0).text = severity
                    table.cell(row_idx, 1).text = str(count)
                else:
                    row = table.add_row()
                    row.cells[0].text = severity
                    row.cells[1].text = str(count)
                row_idx += 1
            break

    # Generate a pie chart based on the vulnerability statistics
    labels = [label for label, count in severity_counts.items() if count > 0]
    sizes = [count for count in severity_counts.values() if count > 0]
    colors = ['#800000', '#FF0000', '#FFA500', '#0000FF', '#008000', '#000000'][:len(labels)]
    
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Vulnerability Severity Distribution')
    
    # Save the pie chart to a BytesIO object
    pie_chart_stream = io.BytesIO()
    plt.savefig(pie_chart_stream, format='png')
    pie_chart_stream.seek(0)

    # Replace the default chart in the template with the new pie chart
    for paragraph in doc.paragraphs:
        if '{TECHNICAL_SUMMARY_CHART}' in paragraph.text:
            paragraph.text = ''
            run = paragraph.add_run()
            run.add_picture(pie_chart_stream, width=Inches(4.5))
            break

    # Update the table of contents
    doc.add_paragraph('Table of Contents', style='Heading 1')
    toc = doc.add_paragraph()
    toc_run = toc.add_run()
    for i, vuln in enumerate(vulnerabilities, start=1):
        toc_run.add_text(f"{i}. {vuln['vulnerability_name']}\n")
        toc_run.font.size = Pt(12)

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
        'poc': 'Use this to bypass authentication.'
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

generate_pentest_report('Sample Pentest Report', '2024-01-01', 'John Doe', vulnerabilities)