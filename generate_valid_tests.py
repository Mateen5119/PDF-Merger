from PyPDF2 import PdfWriter

writer = PdfWriter()
writer.add_blank_page(width=72, height=72)
with open(r'x:\PDF-Merger\test1.pdf', 'wb') as f:
    writer.write(f)

writer2 = PdfWriter()
writer2.add_blank_page(width=72, height=72)
with open(r'x:\PDF-Merger\test2.pdf', 'wb') as f:
    writer2.write(f)
print("Generated valid PDFs using PyPDF2")
