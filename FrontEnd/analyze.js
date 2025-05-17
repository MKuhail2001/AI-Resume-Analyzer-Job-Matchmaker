// Initialize AOS
AOS.init({
    duration: 800,
    easing: 'ease-in-out',
    once: true
});

// Get DOM elements
const uploadForm = document.getElementById('uploadForm');
const spinner = document.getElementById('loadingSpinner');
const navbar = document.querySelector('.navbar');

// Handle sticky navigation
let lastScroll = 0;
window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll <= 0) {
        navbar.classList.remove('hidden');
        return;
    }

    if (currentScroll > lastScroll && !navbar.classList.contains('hidden')) {
        navbar.classList.add('hidden');
    } else if (currentScroll < lastScroll && navbar.classList.contains('hidden')) {
        navbar.classList.remove('hidden');
    }

    lastScroll = currentScroll;
});

// Handle file upload and send to backend
uploadForm.addEventListener('submit', function (e) {
    e.preventDefault();

    const fileInput = document.getElementById('resumeFile');
    if (fileInput.files.length > 0) {
        spinner.style.display = 'block';

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        fetch("http://127.0.0.1:8000/analyze-resume/", {
            method: "POST",
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                spinner.style.display = 'none';
                if (data.analysis) {
                    localStorage.setItem('resumeAnalysis', data.analysis);
                    window.location.href = 'results.html';
                } else {
                    alert('❌ Resume analysis failed.');
                }
            })
            .catch(error => {
                spinner.style.display = 'none';
                alert("🚨 Error during analysis.");
                console.error(error);
            });
    }
});

// Drag-and-drop support
const uploadBox = document.querySelector('.upload-box');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    uploadBox.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    uploadBox.classList.add('bg-light');
});

['dragleave', 'drop'].forEach(eventName => {
    uploadBox.classList.remove('bg-light');
});

uploadBox.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;

    if (files.length > 0) {
        const fileInput = document.getElementById('resumeFile');
        fileInput.files = files;
        uploadForm.dispatchEvent(new Event('submit'));
    }
}
