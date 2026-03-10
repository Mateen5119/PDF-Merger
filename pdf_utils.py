import io
import PyPDF2
from PyPDF2 import PdfMerger
import spire.pdf as spDF

def parse_page_ranges(range_str, max_pages):
    if not range_str or not range_str.strip():
        return list(range(max_pages))
    
    pages = set()
    parts = range_str.split(',')
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            try:
                start, end = part.split('-', 1)
                start_idx = int(start.strip()) - 1
                end_idx = int(end.strip()) - 1
                start_idx = max(0, start_idx)
                end_idx = min(max_pages - 1, end_idx)
                if start_idx <= end_idx:
                    for i in range(start_idx, end_idx + 1):
                        pages.add(i)
            except ValueError:
                pass
        else:
            try:
                idx = int(part) - 1
                if 0 <= idx < max_pages:
                    pages.add(idx)
            except ValueError:
                pass
    return sorted(list(pages)) if pages else list(range(max_pages))

def merge_pdfs(file_list, pages_list=None):
    """
    Merges a list of PDF file-like objects or paths.
    Returns an io.BytesIO containing the merged PDF.
    """
    if not pages_list or len(pages_list) != len(file_list):
        pages_list = [""] * len(file_list)

    writer = PyPDF2.PdfWriter() if hasattr(PyPDF2, 'PdfWriter') else PyPDF2.PdfFileWriter()
    Reader = PyPDF2.PdfReader if hasattr(PyPDF2, 'PdfReader') else PyPDF2.PdfFileReader
    
    for file, page_str in zip(file_list, pages_list):
        reader = Reader(file)
        max_pages = len(reader.pages) if hasattr(reader, 'pages') else reader.getNumPages()
        
        pages_to_add = parse_page_ranges(page_str, max_pages)
        for p in pages_to_add:
            page = reader.pages[p] if hasattr(reader, 'pages') else reader.getPage(p)
            if hasattr(writer, 'add_page'):
                writer.add_page(page)
            else:
                writer.addPage(page)
    
    output_buffer = io.BytesIO()
    writer.write(output_buffer)
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
