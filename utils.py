from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from datetime import datetime
from docx.opc.constants import RELATIONSHIP_TYPE as RT
import pypandoc
import tempfile
import os

def set_font_size_paragraph(paragraph, font, size):
    for run in paragraph.runs:
        run.font.name = font
        run.font.size = Pt(size)

def add_html_after_paragraph(doc, paragraph_text, html, target_paragraph):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
        temp_filename = temp_file.name
        pypandoc.convert_text(html, 'docx', format='html', outputfile=temp_filename)

    temp_doc = Document(temp_filename)

    current_paragraph_element = target_paragraph._element
    for temp_paragraph in temp_doc.paragraphs:
        set_font_size_paragraph(temp_paragraph, "Calibri", 14)
        new_paragraph_element = OxmlElement('w:p')
        new_paragraph_element.extend(temp_paragraph._element)
        current_paragraph_element.addnext(new_paragraph_element)
        current_paragraph_element = new_paragraph_element

    os.remove(temp_filename)

def format_date_range(start_date, end_date):
    if start_date.month == end_date.month:
        return f"{start_date.strftime('%-d')}-{end_date.strftime('%-d %B %Y')}"
    return f"{start_date.strftime('%-d %B')}-{end_date.strftime('%-d %B %Y')}"

def remove_empty_pages(doc):
    for paragraph in doc.paragraphs:
        if paragraph._element.xpath('.//w:br[@w:type="page"]') and not paragraph.text.strip():
            parent = paragraph._element.getparent()
            parent.remove(paragraph._element)

def add_toc(doc, paragraph):
    run = paragraph.add_run("Table of Contents")
    run.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER 
    run.font.name = 'Calibri'
    run.font.size = Pt(14)
    run.bold = True
    run.underline = True

    fldChar = OxmlElement('w:fldChar')
    fldChar.set(qn('w:fldCharType'), 'begin')

    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = 'TOC \\o "1-3" \\h \\z \\u'

    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')

    fldChar3 = OxmlElement('w:updateFields')
    fldChar3.set(qn('w:val'), 'true')
    fldChar2.append(fldChar3)

    fldChar4 = OxmlElement('w:fldChar')
    fldChar4.set(qn('w:fldCharType'), 'end')

    r_element = run._r
    r_element.extend([fldChar, instrText, fldChar2, fldChar4])

    update_fields = OxmlElement('w:updateFields')
    update_fields.set(qn('w:val'), 'true')
    doc.element.body.insert(0, update_fields)
