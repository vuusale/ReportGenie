import docx

infile = 'demo.docx'
doc = docx.Document(infile)
print(doc, dir(doc))
for item in doc.paragraphs:
    print(dir(item))

document = docx.Document()
r = 2 # Number of rows you want
c = 2 # Number of collumns you want
table = document.add_table(rows=r, cols=c)
table.style = 'LightShading-Accent1' # set your style, look at the help documentation for more help
document.save('demo2.docx') # Save document