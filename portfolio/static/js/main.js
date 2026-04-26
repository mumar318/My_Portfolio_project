// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function () {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function () {
            mobileMenu.classList.toggle('hidden');

            // Toggle icon
            const icon = mobileMenuBtn.querySelector('[data-lucide]');
            if (icon) {
                const currentIcon = icon.getAttribute('data-lucide');
                icon.setAttribute('data-lucide', currentIcon === 'menu' ? 'x' : 'menu');
                lucide.createIcons();
            }
        });

        // Close mobile menu when clicking on a link
        const mobileLinks = mobileMenu.querySelectorAll('a');
        mobileLinks.forEach(link => {
            link.addEventListener('click', function () {
                mobileMenu.classList.add('hidden');
                const icon = mobileMenuBtn.querySelector('[data-lucide]');
                if (icon) {
                    icon.setAttribute('data-lucide', 'menu');
                    lucide.createIcons();
                }
            });
        });
    }

    // Navbar scroll effect
    const navbar = document.getElementById('navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
                navbar.style.backdropFilter = 'blur(20px)';
                navbar.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
                navbar.style.borderBottom = '1px solid rgba(107, 114, 128, 0.5)';
                navbar.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.3)';
            } else {
                navbar.classList.remove('scrolled');
                navbar.style.backdropFilter = 'blur(12px)';
                navbar.style.backgroundColor = 'rgba(0, 0, 0, 0.3)';
                navbar.style.borderBottom = '1px solid rgba(107, 114, 128, 0.3)';
                navbar.style.boxShadow = 'none';
            }
        });
    }

    // Smooth scroll for anchor links
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

    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-in').forEach(el => {
        observer.observe(el);
    });

    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // Theme toggle handling (desktop + mobile)
    function syncThemeToggleState() {
        const isDark = document.documentElement.classList.contains('dark');
        document.querySelectorAll('#theme-toggle, #theme-toggle-mobile').forEach(btn => {
            if (!btn) return;
            const moon = btn.querySelector('.theme-icon-dark');
            const sun = btn.querySelector('.theme-icon-light');
            if (moon && sun) {
                if (isDark) {
                    moon.classList.add('hidden');
                    sun.classList.remove('hidden');
                } else {
                    sun.classList.add('hidden');
                    moon.classList.remove('hidden');
                }
            }
        });
    }

    function toggleTheme() {
        const isDark = document.documentElement.classList.toggle('dark');
        try {
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        } catch (e) {
            // ignore storage issues
        }
        syncThemeToggleState();
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    ['theme-toggle', 'theme-toggle-mobile'].forEach(id => {
        const btn = document.getElementById(id);
        if (btn) {
            btn.addEventListener('click', toggleTheme);
        }
    });

    syncThemeToggleState();

    // Add animation delay to elements
    document.querySelectorAll('.fade-in').forEach((el, index) => {
        if (!el.style.animationDelay) {
            el.style.animationDelay = `${index * 0.1}s`;
        }
    });

    // Skill bars animation on scroll
    const skillBars = document.querySelectorAll('.skill-bar');
    if (skillBars.length > 0) {
        const skillObserver = new IntersectionObserver(function (entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'skillBarGrow 1s ease-out forwards';
                }
            });
        }, { threshold: 0.5 });

        skillBars.forEach(bar => {
            skillObserver.observe(bar);
        });
    }

    // Copy email to clipboard functionality
    const emailLinks = document.querySelectorAll('a[href^="mailto:"]');
    emailLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            const email = this.getAttribute('href').replace('mailto:', '');

            // Try to copy to clipboard
            if (navigator.clipboard) {
                navigator.clipboard.writeText(email).then(() => {
                    showNotification('Email copied to clipboard!', 'success');
                }).catch(() => {
                    // Fallback: let the default mailto: behavior work
                });
            }
        });
    });

    // Show notification function
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-20 right-4 z-50 px-6 py-3 rounded-lg shadow-lg text-white font-semibold transition-all duration-300 ${type === 'success' ? 'bg-green-500' :
            type === 'error' ? 'bg-red-500' :
                'bg-blue-500'
            }`;
        notification.textContent = message;
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateX(0)';
        }, 10);

        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    // Add hover effect to project cards
    const projectCards = document.querySelectorAll('.project-card');
    projectCards.forEach(card => {
        card.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });

        card.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Lazy load images
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // Console message
    console.log('%c👋 Welcome to my portfolio!', 'color: #6366f1; font-size: 20px; font-weight: bold;');
    console.log('%cBuilt with Django & Tailwind CSS', 'color: #8b5cf6; font-size: 14px;');
    console.log('%cInterested in working together? Contact me!', 'color: #10b981; font-size: 14px;');
});

// Handle page visibility change
document.addEventListener('visibilitychange', function () {
    const originalTitle = document.title;
    if (document.hidden) {
        document.title = '👋 Come back!';
    } else {
        document.title = originalTitle;
    }
});

// Add keyboard navigation
document.addEventListener('keydown', function (e) {
    // Press 'H' to go home
    if (e.key === 'h' || e.key === 'H') {
        if (!e.target.matches('input, textarea')) {
            window.location.href = '/';
        }
    }

    // Press 'C' to go to contact
    if (e.key === 'c' || e.key === 'C') {
        if (!e.target.matches('input, textarea')) {
            window.location.href = '/contact/';
        }
    }

    // Press 'P' to go to projects
    if (e.key === 'p' || e.key === 'P') {
        if (!e.target.matches('input, textarea')) {
            window.location.href = '/projects/';
        }
    }
});
