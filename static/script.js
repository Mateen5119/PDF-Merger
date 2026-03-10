const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const gallery = document.getElementById('gallery');
const btnMerge = document.getElementById('btn-merge');
const progressContainer = document.querySelector('.progress-container');
const progressBar = document.getElementById('upload-progress');
const progressText = document.getElementById('progress-text');

let selectedFiles = [];

// Prevent default drag behaviors
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Highlight drop area 
['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => dropArea.classList.add('highlight'), false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => dropArea.classList.remove('highlight'), false);
});

// Select files
dropArea.addEventListener('drop', handleDrop, false);
fileInput.addEventListener('change', handleFiles, false);
dropArea.addEventListener('click', () => {
    // If they click the drop area, they can click the label as well but this makes the whole area clickable
    if (event.target.tagName !== 'LABEL' && event.target.tagName !== 'INPUT') {
        fileInput.click();
    }
});

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles({ target: { files: files } });
}

function handleFiles(e) {
    const files = [...e.target.files];
    const pdfs = files.filter(f => f.type === 'application/pdf' || f.name.toLowerCase().endsWith('.pdf'));

    if (pdfs.length > 0) {
        selectedFiles = [...selectedFiles, ...pdfs];
        updateGallery(pdfs);
        updateActions();
    }
}

function updateGallery(newFiles) {
    newFiles.forEach(file => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = function () {
            const div = document.createElement('div');
            div.className = 'pdf-item';
            div.innerHTML = `
                <svg viewBox="0 0 24 24">
                    <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-9.5 8.5H8v2H6v-5h3.5c1.1 0 2 .9 2 2 0 1.1-.9 2-2 2zm4.5 2.5h-3v-5h3c1.1 0 2 .9 2 2s-.9 2-2 2zm4-1.5h-2v1.5h-1.5v-5H18v1.5h-2v1.5h2v1.5z"></path>
                </svg>
                <div style="display: flex; flex-direction: column; align-items: center; width: 100%;">
                    <div class="pdf-name" style="margin-bottom: 5px;">${file.name}</div>
                    <input type="text" class="page-input" placeholder="Pages (e.g. 1, 3-5)" style="width: 80%; padding: 4px; border: 1px solid #ccc; border-radius: 4px; font-size: 12px; text-align: center; color: black;" onclick="event.stopPropagation()">
                </div>
            `;
            gallery.appendChild(div);
        };
    });
}

function updateActions() {
    btnMerge.disabled = selectedFiles.length < 2;
}

btnMerge.addEventListener('click', () => {
    if (selectedFiles.length < 2) return;

    const formData = new FormData();
    const pageInputs = document.querySelectorAll('.page-input');

    selectedFiles.forEach((file, index) => {
        formData.append('pdfs', file);
        if (pageInputs[index]) {
            formData.append('pages', pageInputs[index].value);
        } else {
            formData.append('pages', '');
        }
    });

    const xhr = new XMLHttpRequest();

    xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
            const percentComplete = Math.round((e.loaded / e.total) * 100);
            progressContainer.classList.add('active');
            progressBar.value = percentComplete;
            progressText.innerText = percentComplete + '%';
        }
    });

    xhr.addEventListener('load', () => {
        if (xhr.status === 200) {
            const blob = xhr.response;

            // Try Pywebview native API to avoid silent failure of Object URL downloads
            if (window.pywebview && window.pywebview.api) {
                const reader = new FileReader();
                reader.readAsDataURL(blob);
                reader.onloadend = function () {
                    const base64data = reader.result.split(',')[1];
                    window.pywebview.api.save_pdf(base64data).then(res => {
                        console.log(res);
                        progressBar.value = 100;
                        progressText.innerText = "Merge Complete!";
                        setTimeout(() => {
                            progressContainer.classList.remove('active');
                            progressBar.value = 0;
                        }, 3000);
                    }).catch(err => {
                        console.error("Save error:", err);
                        alert('Error saving PDF: ' + err);
                        progressContainer.classList.remove('active');
                    });
                };
            } else {
                // Fallback for normal browser
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = 'merged.pdf';
                document.body.appendChild(a);
                a.click();

                setTimeout(() => {
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                }, 5000);

                progressBar.value = 100;
                progressText.innerText = "Merge Complete!";
                setTimeout(() => {
                    progressContainer.classList.remove('active');
                    progressBar.value = 0;
                }, 3000);
            }
        } else {
            alert('Error merging PDFs.');
            progressContainer.classList.remove('active');
        }
    });

    xhr.addEventListener('error', () => {
        alert('Network Error.');
        progressContainer.classList.remove('active');
    });

    xhr.open('POST', '/merge_PDFs', true);
    xhr.responseType = 'blob'; // To handle binary PDF data
    xhr.send(formData);
});
