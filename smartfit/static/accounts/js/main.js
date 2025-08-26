// SmartFit Main JavaScript File

// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    const scrollLinks = document.querySelectorAll('a[href^="#"]');
    
    for (const scrollLink of scrollLinks) {
        scrollLink.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    }
    
    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Add animation classes on scroll
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    if (animatedElements.length > 0) {
        const animateOnScroll = function() {
            for (const element of animatedElements) {
                const elementPosition = element.getBoundingClientRect().top;
                const windowHeight = window.innerHeight;
                
                if (elementPosition < windowHeight - 100) {
                    element.classList.add('animated');
                }
            }
        };
        
        window.addEventListener('scroll', animateOnScroll);
        animateOnScroll(); // Run once on page load
    }
});

// Testimonial slider functionality
function initTestimonialSlider() {
    const testimonials = document.querySelectorAll('.testimonial-card');
    if (testimonials.length <= 3) return;
    
    let currentIndex = 0;
    const maxIndex = testimonials.length - 3;
    
    const prevButton = document.getElementById('testimonial-prev');
    const nextButton = document.getElementById('testimonial-next');
    
    if (prevButton && nextButton) {
        prevButton.addEventListener('click', function() {
            if (currentIndex > 0) {
                currentIndex--;
                updateTestimonialSlider();
            }
        });
        
        nextButton.addEventListener('click', function() {
            if (currentIndex < maxIndex) {
                currentIndex++;
                updateTestimonialSlider();
            }
        });
        
        function updateTestimonialSlider() {
            for (let i = 0; i < testimonials.length; i++) {
                if (i >= currentIndex && i < currentIndex + 3) {
                    testimonials[i].style.display = 'block';
                } else {
                    testimonials[i].style.display = 'none';
                }
            }
            
            prevButton.disabled = currentIndex === 0;
            nextButton.disabled = currentIndex === maxIndex;
        }
        
        updateTestimonialSlider();
    }
}

// Initialize testimonial slider on larger screens
window.addEventListener('load', function() {
    if (window.innerWidth >= 768) {
        initTestimonialSlider();
    }
});

window.addEventListener('resize', function() {
    if (window.innerWidth >= 768) {
        initTestimonialSlider();
    }
});
