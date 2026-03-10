import os
import sys
import threading
from flask import Flask, render_template, request, send_file
import webview
from pdf_utils import merge_pdfs, split_pdf

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = Flask(__name__, 
            template_folder=resource_path('templates'),
            static_folder=resource_path('static'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge_PDFs', methods=['POST'])
def merge_pdfs_route():
    if 'pdfs' not in request.files:
        return "No file part", 400
    
    files = request.files.getlist('pdfs')
    pages_list = request.form.getlist('pages')
    if not files:
        return "No selected file", 400
    
    try:
        buffer = merge_pdfs(files, pages_list)
        return send_file(
            buffer,
            as_attachment=True,
            download_name='merged.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        print(f"Error merging: {e}")
        return str(e), 500

import base64

class API:
    def get_info(self):
        return "PDF Toolchain API Initialized."

    def save_pdf(self, b64_data):
        try:
            window = webview.windows[0]
            result = window.create_file_dialog(
                webview.SAVE_DIALOG, 
                directory='', 
                save_filename='merged.pdf'
            )
            if result:
                file_path = result if isinstance(result, str) else result[0]
                with open(file_path, 'wb') as f:
                    f.write(base64.b64decode(b64_data))
                return f"Saved to {file_path}"
            return "Save cancelled"
        except Exception as e:
            print(f"Error saving PDF: {e}")
            return str(e)

def start_server():
    app.run(host='127.0.0.1', port=5000, threaded=True)

if __name__ == '__main__':
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()
    
    api = API()
    webview.create_window('Antigravity PDF Toolchain', 'http://127.0.0.1:5000', js_api=api, width=900, height=700)
    webview.start()
