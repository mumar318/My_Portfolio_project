// About page - Tab switching functionality
document.addEventListener('DOMContentLoaded', function () {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    // Apply animation delays from data attributes
    document.querySelectorAll('[data-delay]').forEach(el => {
        el.style.animationDelay = el.dataset.delay + 's';
    });

    // Initialize skill bars with staggered animation
    const animateSkillBars = () => {
        const skillBars = document.querySelectorAll('.skill-bar');
        skillBars.forEach((bar, index) => {
            const width = bar.getAttribute('data-width');
            if (width) {
                setTimeout(() => {
                    bar.style.width = width + '%';
                }, index * 50); // Stagger animation by 50ms
            }
        });
    };

    // Animate on page load
    setTimeout(animateSkillBars, 300);

    // Re-animate when skills tab is clicked
    const skillsTab = document.querySelector('[data-tab="skills"]');
    if (skillsTab) {
        skillsTab.addEventListener('click', () => {
            setTimeout(() => {
                const skillBars = document.querySelectorAll('.skill-bar');
                skillBars.forEach(bar => {
                    bar.style.width = '0%';
                });
                setTimeout(animateSkillBars, 100);
            }, 100);
        });
    }

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;

            // Update button styles
            tabBtns.forEach(b => {
                b.classList.remove('active', 'bg-gradient-to-r', 'from-blue-500', 'to-purple-500', 'text-white', 'shadow-lg');
                b.classList.add('text-gray-600', 'dark:text-gray-400', 'hover:text-gray-900', 'dark:hover:text-white', 'hover:bg-gray-50', 'dark:hover:bg-gray-700');
            });
            btn.classList.add('active', 'bg-gradient-to-r', 'from-blue-500', 'to-purple-500', 'text-white', 'shadow-lg');
            btn.classList.remove('text-gray-600', 'dark:text-gray-400', 'hover:text-gray-900', 'dark:hover:text-white', 'hover:bg-gray-50', 'dark:hover:bg-gray-700');

            // Show/hide content
            tabContents.forEach(content => {
                content.classList.add('hidden');
            });

            const targetTab = document.getElementById(`${tabName}-tab`);
            if (targetTab) {
                targetTab.classList.remove('hidden');
            }
        });
    });
});
