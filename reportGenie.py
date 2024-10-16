from docx import Document
from docx.shared import RGBColor, Pt
from docx.enum.text import WD_LINE_SPACING, WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import matplotlib.pyplot as plt
import io
from docx.shared import Inches

def generate_pentest_report(report_title, date, reporter_name, vulnerabilities, icon_path):
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

    # Insert icon image at the placeholder and make it larger
    for paragraph in doc.paragraphs:
        if '{ICON}' in paragraph.text:
            paragraph.text = ''
            run = paragraph.add_run()
            run.add_picture(icon_path, width=Inches(3.5))  # Make the logo large enough to take half of the page width
            run.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            paragraph_format = paragraph.paragraph_format
            paragraph_format.space_after = Pt(18)  # 1.5 line spacing after the logo
            break

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
        vulnerable_component_run = vulnerable_component_paragraph.add_run("URL/Vulnerable component: ")
        vulnerable_component_run.bold = True
        vulnerable_component_value_run = vulnerable_component_paragraph.add_run(vuln['vulnerable_component'])
        vulnerable_component_paragraph.paragraph_format.line_spacing = 1.5

        # Add description
        description_paragraph = doc.add_paragraph()
        description_run = description_paragraph.add_run("Description: ")
        description_run.bold = True
        description_value_run = description_paragraph.add_run(vuln['description'])
        description_paragraph.paragraph_format.line_spacing = 1.5

        # Add impact
        impact_paragraph = doc.add_paragraph()
        impact_run = impact_paragraph.add_run("Impact: ")
        impact_run.bold = True
        impact_value_run = impact_paragraph.add_run(vuln['impact'])
        impact_paragraph.paragraph_format.line_spacing = 1.5

        # Add remediation
        remediation_paragraph = doc.add_paragraph()
        remediation_run = remediation_paragraph.add_run("Remediation: ")
        remediation_run.bold = True
        remediation_value_run = remediation_paragraph.add_run(vuln['remediation'])
        remediation_paragraph.paragraph_format.line_spacing = 1.5

        # Add PoC
        poc_paragraph = doc.add_paragraph()
        poc_run = poc_paragraph.add_run("PoC: ")
        poc_run.bold = True
        poc_value_run = poc_paragraph.add_run(vuln['poc'])
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

    # Find and update the placeholders in the table with severity counts
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if '{CRITICAL}' in cell.text:
                    cell.text = cell.text.replace('{CRITICAL}', str(severity_counts['Critical']))
                    cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                if '{HIGH}' in cell.text:
                    cell.text = cell.text.replace('{HIGH}', str(severity_counts['High']))
                    cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                if '{MEDIUM}' in cell.text:
                    cell.text = cell.text.replace('{MEDIUM}', str(severity_counts['Medium']))
                    cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                if '{LOW}' in cell.text:
                    cell.text = cell.text.replace('{LOW}', str(severity_counts['Low']))
                    cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                if '{INFORMATIONAL}' in cell.text:
                    cell.text = cell.text.replace('{INFORMATIONAL}', str(severity_counts['Informational']))
                    cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                if '{TOTAL}' in cell.text:
                    cell.text = cell.text.replace('{TOTAL}', str(sum(severity_counts.values())))
                    cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

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
            run.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            break

    # Insert table of contents at the placeholder
    for paragraph in doc.paragraphs:
        if '{TABLE_OF_CONTENTS}' in paragraph.text:
            paragraph.text = ''
            toc_paragraph = doc.add_paragraph()
            toc_paragraph.add_run('Table of Contents').bold = True
            toc_paragraph.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            for i, vuln in enumerate(vulnerabilities, start=1):
                toc_entry = doc.add_paragraph()
                toc_entry.add_run(f"{i}. {vuln['vulnerability_name']}").bold = False
            break

    # Add icon image to the header on all pages
    for section in doc.sections:
        header = section.header
        header_paragraph = header.paragraphs[0]
        header_paragraph.text = ''
        header_run = header_paragraph.add_run()
        header_run.add_picture(icon_path, width=Inches(1.0))
        header_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        header_paragraph.paragraph_format.line_spacing = 1.5

    # Align project title, date, and reporter name to bottom left of the first page
    for paragraph in doc.paragraphs:
        if '{REPORT_TITLE}' in paragraph.text or '{DATE}' in paragraph.text or '{REPORTER_NAME}' in paragraph.text:
            paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
            paragraph.paragraph_format.space_before = Pt(600)  # Push text to bottom

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

# Provide the path to your icon image
icon_path = 'icon.png'

generate_pentest_report('Sample Pentest Report', '2024-01-01', 'John Doe', vulnerabilities, icon_path)
