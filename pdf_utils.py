import io
import PyPDF2
from PyPDF2 import PdfMerger
import spire.pdf as spDF

def merge_pdfs(file_list):
    """
    Merges a list of PDF file-like objects or paths.
    Returns an io.BytesIO containing the merged PDF.
    """
    merger = PdfMerger()
    for file in file_list:
        merger.append(file)
    
    output_buffer = io.BytesIO()
    merger.write(output_buffer)
    merger.close()
    
    output_buffer.seek(0)
    return output_buffer

def split_pdf(file_path, output_prefix="split_page_"):
    """
    Splits a target PDF into multiple single-page PDFs using Spire.PDF.
    """
    document = spDF.PdfDocument()
    if isinstance(file_path, str):
        document.LoadFromFile(file_path)
    else:
        document.LoadFromBytes(file_path.read())
    
    page_count = document.Pages.Count
    document.Split(output_prefix + "{0}.pdf", 1)
    
    document.Close()
    
    return [f"{output_prefix}{i}.pdf" for i in range(page_count)]
