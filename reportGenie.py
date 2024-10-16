from docx import Document
from docx.shared import RGBColor, Pt
from docx.enum.text import WD_LINE_SPACING, WD_PARAGRAPH_ALIGNMENT
import matplotlib.pyplot as plt
import io
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
        severity_value_run.bold = True
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
            # First row with one column (empty placeholder row)
            table.cell(0, 0).text = ""
            table.cell(0, 0).paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

            # Second row with severity labels
            severity_labels = [
                ('Critical', RGBColor(128, 0, 0)),  # Burgundy
                ('High', RGBColor(255, 0, 0)),       # Red
                ('Medium', RGBColor(255, 165, 0)),   # Orange
                ('Low', RGBColor(0, 0, 255)),        # Blue
                ('Informational', RGBColor(0, 128, 0)), # Green
                ('Total', RGBColor(128, 0, 128))     # Purple
            ]
            for idx, (label, color) in enumerate(severity_labels):
                cell = table.cell(1, idx)
                run = cell.paragraphs[0].add_run(label)
                run.bold = True
                run.font.color.rgb = color
                cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

            # Third row with severity counts
            counts = [
                severity_counts['Critical'],
                severity_counts['High'],
                severity_counts['Medium'],
                severity_counts['Low'],
                severity_counts['Informational'],
                sum(severity_counts.values())
            ]
            for idx, count in enumerate(counts):
                cell = table.cell(2, idx)
                run = cell.paragraphs[0].add_run(str(count))
                run.bold = True
                cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            break

    # Generate a pie chart based on the vulnerability statistics
    labels = [label for label, count in severity_counts.items() if count > 0]
    sizes = [count for count in severity_counts.values() if count > 0]
    colors = ['#800000', '#FF0000', '#FFA500', '#0000FF', '#008000', '#800080'][:len(labels)]
    
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