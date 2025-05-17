// Initialize AOS (Animate On Scroll)
AOS.init({
    duration: 800,
    easing: 'ease-in-out',
    once: true
});

// Get DOM elements
const uploadForm = document.getElementById('uploadForm');
const spinner = document.getElementById('loadingSpinner');
const preview = document.getElementById('resumePreview');
const generateBtn = document.getElementById('generateBtn');
const downloadBtn = document.getElementById('downloadBtn');
const downloadSection = document.getElementById('downloadSection');
const navbar = document.querySelector('.navbar');
const navLinks = document.querySelectorAll('.nav-link');

// Add initial hidden class to sections except landing
document.querySelectorAll('#summary, #improvements, #matching, #career, #downloadSection').forEach(section => {
    section.classList.add('section-hidden');
});

// Handle sticky navigation
let lastScroll = 0;
window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    // Show/hide navbar based on scroll direction
    if (currentScroll <= 0) {
        navbar.classList.remove('hidden');
        return;
    }
    
    if (currentScroll > lastScroll && !navbar.classList.contains('hidden')) {
        // Scrolling down
        navbar.classList.add('hidden');
    } else if (currentScroll < lastScroll && navbar.classList.contains('hidden')) {
        // Scrolling up
        navbar.classList.remove('hidden');
    }
    
    lastScroll = currentScroll;
});

// Update active nav link based on scroll position
function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const scrollY = window.pageYOffset;
    
    sections.forEach(section => {
        const sectionHeight = section.offsetHeight;
        const sectionTop = section.offsetTop - 100;
        const sectionId = section.getAttribute('id');
        
        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            document.querySelector('.nav-link[href*=' + sectionId + ']')?.classList.add('active');
        } else {
            document.querySelector('.nav-link[href*=' + sectionId + ']')?.classList.remove('active');
        }
    });
}

window.addEventListener('scroll', updateActiveNavLink);

// Handle file upload and analysis
uploadForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('resumeFile');
    
    if (fileInput.files.length > 0) {
        // Show loading spinner
        spinner.style.display = 'block';
        
        // Simulate file processing
        setTimeout(() => {
            // Hide loading spinner
            spinner.style.display = 'none';
            
            // Navigate to results page
            window.location.href = 'results.html';
        }, 2000);
    }
});

// Handle generate improved resume button
generateBtn.addEventListener('click', function() {
    // Show loading state
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Generating...';
    
    // Simulate generation process (replace with actual API call)
    setTimeout(() => {
        // Reset button state
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<i class="bi bi-stars"></i> Generate Improved Resume';
        
        // Show download section
        downloadSection.classList.remove('section-hidden');
        downloadBtn.style.display = 'inline-block';
        
        // Create and set download link (replace with actual file generation)
        const blob = new Blob(["Improved resume content..."], { type: 'application/pdf' });
        const url = URL.createObjectURL(blob);
        downloadBtn.href = url;
        
        // Smooth scroll to download section
        document.getElementById('downloadSection').scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }, 2000);
});

// Add smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Check if user is trying to access home section directly
window.addEventListener('load', function() {
    const hash = window.location.hash;
    if (hash === '#home') {
        // Scroll to landing page first
        window.scrollTo(0, 0);
        // Remove the hash
        history.pushState("", document.title, window.location.pathname);
    }
}); 