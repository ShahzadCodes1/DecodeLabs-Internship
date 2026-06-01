/* ===========================
   MOBILE NAVIGATION
   =========================== */

const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        navLinks?.classList.toggle('active');
        hamburger.classList.toggle('active');
    });
}

// Close mobile menu when link is clicked
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks?.classList.remove('active');
        hamburger?.classList.remove('active');
    });
});

/* ===========================
   SCROLL ANIMATIONS
   =========================== */

// Intersection Observer for fade-in animations on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'slideInUp 0.8s ease-out forwards';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all service cards, feature cards, and testimonial cards
document.querySelectorAll('.service-card, .feature-card, .testimonial-card').forEach(card => {
    observer.observe(card);
});

/* ===========================
   NAVBAR BACKGROUND ON SCROLL
   =========================== */

const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar?.style.background = 'rgba(5, 8, 18, 0.95)';
    } else {
        navbar?.style.background = 'rgba(5, 8, 18, 0.8)';
    }
});

/* ===========================
   SMOOTH SCROLL BEHAVIOR FOR BUTTONS
   =========================== */

// Already handled in HTML with inline onclick, but adding smooth scroll enhancement
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && document.querySelector(href)) {
            e.preventDefault();
            const target = document.querySelector(href);
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

/* ===========================
   ADD SLIDEUP ANIMATION
   =========================== */

const style = document.createElement('style');
style.textContent = `
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

/* ===========================
   PARALLAX EFFECT ON HERO
   =========================== */

const heroSection = document.querySelector('.hero');
const glowOrbs = document.querySelectorAll('.glow-orb');

window.addEventListener('mousemove', (e) => {
    if (!heroSection || window.innerWidth < 768) return;
    
    const mouseX = e.clientX / window.innerWidth;
    const mouseY = e.clientY / window.innerHeight;
    
    glowOrbs.forEach((orb, index) => {
        const moveX = mouseX * (index + 1) * 20;
        const moveY = mouseY * (index + 1) * 20;
        orb.style.transform = `translate(${moveX}px, ${moveY}px)`;
    });
});

/* ===========================
   COUNTER ANIMATION
   =========================== */

function animateCounter(element, target, duration = 2000) {
    let current = 0;
    const increment = target / (duration / 16);
    
    const updateCounter = () => {
        current += increment;
        if (current < target) {
            element.textContent = Math.floor(current).toLocaleString();
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target.toLocaleString();
        }
    };
    
    updateCounter();
}

// Animate stats on scroll into view
const statsSection = document.querySelector('.stats');
if (statsSection) {
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const statElements = entry.target.querySelectorAll('.stat h4');
                statElements.forEach(stat => {
                    const target = parseInt(stat.textContent.replace(/[^0-9]/g, '')) || 0;
                    if (target > 0) {
                        animateCounter(stat, target);
                    }
                });
                statsObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    statsObserver.observe(statsSection);
}

/* ===========================
   ACTIVE NAV LINK HIGHLIGHTING
   =========================== */

const navItems = document.querySelectorAll('.nav-links a[href^="#"]');

window.addEventListener('scroll', () => {
    let current = '';
    
    document.querySelectorAll('section').forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });
    
    navItems.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').slice(1) === current) {
            link.classList.add('active');
        }
    });
});

/* Add active state styling */
const activeStyle = document.createElement('style');
activeStyle.textContent = `
    .nav-links a.active {
        color: var(--primary);
    }
    
    .nav-links a.active::after {
        width: 100%;
    }
`;
document.head.appendChild(activeStyle);

/* ===========================
   CURSOR EFFECT (OPTIONAL)
   =========================== */

// Custom cursor for interactive elements
const interactiveElements = document.querySelectorAll('.btn, a, .service-link');

interactiveElements.forEach(element => {
    element.addEventListener('mouseenter', () => {
        document.body.style.cursor = 'pointer';
    });
    
    element.addEventListener('mouseleave', () => {
        document.body.style.cursor = 'auto';
    });
});

/* ===========================
   PERFORMANCE OPTIMIZATION
   =========================== */

// Lazy load images (if added in future)
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                imageObserver.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

/* ===========================
   FORM HANDLING
   =========================== */

// Handle CTA button click (for future form integration)
const ctaButtons = document.querySelectorAll('.btn-primary');

ctaButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        // Add ripple effect
        const rect = button.getBoundingClientRect();
        const ripple = document.createElement('span');
        ripple.style.position = 'absolute';
        ripple.style.borderRadius = '50%';
        ripple.style.background = 'rgba(255, 255, 255, 0.5)';
        ripple.style.width = ripple.style.height = '20px';
        ripple.style.animation = 'ripple 0.6s ease-out';
        
        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    });
});

// Add ripple animation
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    @keyframes ripple {
        to {
            width: 400px;
            height: 400px;
            opacity: 0;
        }
    }
`;
document.head.appendChild(rippleStyle);

/* ===========================
   INITIALIZATION
   =========================== */

console.log('NeuroSync Landing Page - Loaded Successfully');
console.log('🚀 Ready to launch your AI future!');
