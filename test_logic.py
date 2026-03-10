import io
import sys
from pdf_utils import merge_pdfs

def test():
    try:
        with open(r'x:\PDF-Merger\test1.pdf', 'rb') as f1, open(r'x:\PDF-Merger\test2.pdf', 'rb') as f2:
            files = [f1, f2]
            pages_list = ["1", "1"]
            
            out_buf = merge_pdfs(files, pages_list)
            
            with open(r'x:\PDF-Merger\test_merged_logic.pdf', 'wb') as out:
                out.write(out_buf.read())
                
            print("Logic test passed! Output saved to test_merged_logic.pdf")
    except Exception as e:
        print(f"Test failed with error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    test()
