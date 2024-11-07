from docx import Document
from docx.shared import RGBColor, Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from datetime import datetime
import matplotlib.pyplot as plt
import io
from utils import *

def generate_pentest_report(report_title, start_date, end_date, reporter_name, vulnerabilities, icon_path, executive_summary, output_path):
    doc = Document('report.docx')
    start_date = datetime(*[int(i) for i in start_date.split("-")])
    end_date = datetime(*[int(i) for i in end_date.split("-")])
    date = format_date_range(start_date, end_date)

    for paragraph in doc.paragraphs:
        if '{REPORT_TITLE}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{REPORT_TITLE}', report_title)
        if '{DATE}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{DATE}', date)
        if '{REPORTER_NAME}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{REPORTER_NAME}', reporter_name)
        if '{ICON}' in paragraph.text:
            paragraph.text = ''
            run = paragraph.add_run()
            run.add_picture(icon_path, height=Inches(1.2))
            run.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            paragraph.paragraph_format.space_after = Pt(18)
        if '{TOC}' in paragraph.text:
            paragraph.clear()
            add_toc(doc, paragraph)
        if '{EXECUTIVE_SUMMARY}' in paragraph.text:
            paragraph.text = executive_summary

    for i, vuln in enumerate(vulnerabilities, start=1):
        heading = doc.add_heading(level=2)
        heading.add_run(f"{i}. {vuln.vulnerability_name}")
        heading.paragraph_format.line_spacing = 1.5

        severity_paragraph = doc.add_paragraph()
        severity_paragraph.add_run("Severity: ").bold = True
        severity_value_run = severity_paragraph.add_run(vuln.severity)
        severity_value_run.bold = True
        color_map = {
            'critical': RGBColor(128, 0, 0),
            'high': RGBColor(255, 0, 0),
            'medium': RGBColor(255, 165, 0),
            'low': RGBColor(0, 0, 255),
            'informational': RGBColor(0, 128, 0)
        }
        severity_value_run.font.color.rgb = color_map.get(vuln.severity.lower(), RGBColor(0, 0, 0))
        severity_paragraph.paragraph_format.line_spacing = 1.5

        vulnerable_component_paragraph = doc.add_paragraph()
        vulnerable_component_paragraph.add_run("URL/Vulnerable component: ").bold = True
        vulnerable_component_paragraph.add_run(vuln.vulnerable_component)
        vulnerable_component_paragraph.paragraph_format.line_spacing = 1.5

        description_paragraph = doc.add_paragraph()
        description_paragraph.add_run("Description: ").bold = True
        add_html_after_paragraph(doc, "Description", vuln.description, description_paragraph)

        impact_paragraph = doc.add_paragraph()
        impact_paragraph.paragraph_format.space_before = Pt(8)
        impact_paragraph.add_run("Impact: ").bold = True
        add_html_after_paragraph(doc, 'Impact', vuln.impact, impact_paragraph)

        remediation_paragraph = doc.add_paragraph()
        remediation_paragraph.paragraph_format.space_before = Pt(8)
        remediation_paragraph.add_run("Remediation: ").bold = True
        add_html_after_paragraph(doc, 'Remediation', vuln.remediation, remediation_paragraph)

        poc_paragraph = doc.add_paragraph()
        poc_paragraph.paragraph_format.space_before = Pt(8)
        poc_paragraph.add_run("PoC: ").bold = True
        add_html_after_paragraph(doc, 'PoC', vuln.poc, poc_paragraph)

    severity_counts = {
        'Critical': 0,
        'High': 0,
        'Medium': 0,
        'Low': 0,
        'Informational': 0,
        'Other': 0
    }

    for vuln in vulnerabilities:
        severity = vuln.severity.capitalize()
        if severity in severity_counts:
            severity_counts[severity] += 1
        else:
            severity_counts['Other'] += 1

    labels = [label for label, count in severity_counts.items() if count > 0]
    sizes = [count for count in severity_counts.values() if count > 0]
    colors = ['#800000', '#FF0000', '#FFA500', '#0000FF', '#008000', '#800080'][:len(labels)]

    plt.switch_backend('Agg')
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Vulnerability Severity Distribution\n')

    pie_chart_stream = io.BytesIO()
    plt.savefig(pie_chart_stream, format='png')
    pie_chart_stream.seek(0)

    for paragraph in doc.paragraphs:
        if '{TECHNICAL_SUMMARY_CHART}' in paragraph.text:
            paragraph.text = ''
            run = paragraph.add_run()
            run.add_picture(pie_chart_stream, width=Inches(4.5))
            run.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            break

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if '{CRITICAL}' in cell.text:
                    cell.text = str(severity_counts['Critical'])
                elif '{HIGH}' in cell.text:
                    cell.text = str(severity_counts['High'])
                elif '{MEDIUM}' in cell.text:
                    cell.text = str(severity_counts['Medium'])
                elif '{LOW}' in cell.text:
                    cell.text = str(severity_counts['Low'])
                elif '{INFORMATIONAL}' in cell.text:
                    cell.text = str(severity_counts['Informational'])
                elif '{TOTAL}' in cell.text:
                    cell.text = str(sum(severity_counts.values()))
                cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    for section in doc.sections:
        header_paragraph = section.header.paragraphs[0]
        header_paragraph.text = ''
        header_paragraph.add_run().add_picture(icon_path, height=Inches(0.4))
        header_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        header_paragraph.paragraph_format.line_spacing = 1.5

    for paragraph in doc.paragraphs:
        if '{REPORT_TITLE}' in paragraph.text or '{DATE}' in paragraph.text or '{REPORTER_NAME}' in paragraph.text:
            paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
            paragraph.paragraph_format.space_before = Pt(600)

    doc.save(output_path)
    print(f"Report generated: {output_path}")

vulnerabilities2 = [
    {
        'vulnerability_name': 'a',
        'vulnerable_component': 'http://example.com/login',
        'severity': 'High',
        'description': 'SQL injection vulnerability in login form.',
        'impact': 'Access to all user data.',
        'remediation': 'Use parameterized queries.',
        'poc': 'Use this to bypass authentication.'
    }
]

executive_summary = "a."
icon_path = 'logo.png'

if __name__ == "__main__":
    generate_pentest_report('Sample Pentest Report', '2024-01-01', '2024-01-05', 'John Doe', vulnerabilities2, icon_path, executive_summary)
