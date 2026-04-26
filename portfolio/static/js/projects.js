// Projects page - Filtering and search functionality
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    const clearSearchBtn = document.getElementById('clear-search');
    const categoryBtns = document.querySelectorAll('.category-btn');
    const projectCards = document.querySelectorAll('.project-card');
    const projectCount = document.getElementById('project-count');
    const projectText = document.getElementById('project-text');
    const filterInfo = document.getElementById('filter-info');
    const noResults = document.getElementById('no-results');
    const projectsContainer = document.getElementById('projects-container');
    const gridViewBtn = document.getElementById('grid-view-btn');
    const listViewBtn = document.getElementById('list-view-btn');

    let currentFilter = 'all';
    let currentSearch = '';
    let currentView = 'grid';

    // Apply animation delays from data attributes
    document.querySelectorAll('[data-delay]').forEach(el => {
        const delay = el.dataset.delay;
        if (delay) {
            el.style.animationDelay = (parseFloat(delay) * 0.1) + 's';
        }
    });

    // Search functionality
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            currentSearch = e.target.value.toLowerCase();
            clearSearchBtn.classList.toggle('hidden', !currentSearch);
            filterProjects();
        });
    }

    if (clearSearchBtn) {
        clearSearchBtn.addEventListener('click', () => {
            searchInput.value = '';
            currentSearch = '';
            clearSearchBtn.classList.add('hidden');
            filterProjects();
        });
    }

    // Category filter
    categoryBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            currentFilter = btn.dataset.category;

            // Update button styles
            categoryBtns.forEach(b => {
                b.className = 'category-btn px-4 py-2 rounded-xl font-medium capitalize transition-all duration-300 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600';
            });
            btn.className = 'category-btn px-4 py-2 rounded-xl font-medium capitalize transition-all duration-300 bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg shadow-indigo-500/25';

            filterProjects();
        });
    });

    // View toggle
    if (gridViewBtn) {
        gridViewBtn.addEventListener('click', () => {
            currentView = 'grid';
            projectsContainer.className = 'grid sm:grid-cols-2 lg:grid-cols-3 gap-8';
            gridViewBtn.className = 'p-2 rounded-lg transition-all duration-300 bg-white dark:bg-gray-600 text-indigo-600 shadow-sm';
            listViewBtn.className = 'p-2 rounded-lg transition-all duration-300 text-gray-500 hover:text-gray-700';
        });
    }

    if (listViewBtn) {
        listViewBtn.addEventListener('click', () => {
            currentView = 'list';
            projectsContainer.className = 'grid gap-6 max-w-4xl mx-auto';
            listViewBtn.className = 'p-2 rounded-lg transition-all duration-300 bg-white dark:bg-gray-600 text-indigo-600 shadow-sm';
            gridViewBtn.className = 'p-2 rounded-lg transition-all duration-300 text-gray-500 hover:text-gray-700';
        });
    }

    function filterProjects() {
        let visibleCount = 0;

        projectCards.forEach(card => {
            const title = card.dataset.title;
            const desc = card.dataset.desc;
            const tech = card.dataset.tech;
            const categories = card.dataset.categories.split(',');

            const matchesCategory = currentFilter === 'all' || categories.includes(currentFilter);
            const matchesSearch = !currentSearch ||
                title.includes(currentSearch) ||
                desc.includes(currentSearch) ||
                tech.includes(currentSearch);

            if (matchesCategory && matchesSearch) {
                card.style.display = 'block';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Update count
        if (projectCount) projectCount.textContent = visibleCount;
        if (projectText) projectText.textContent = visibleCount === 1 ? 'project' : 'projects';

        // Update filter info
        let info = '';
        if (currentFilter !== 'all') {
            info += ` in ${currentFilter}`;
        }
        if (currentSearch) {
            info += ` matching "${currentSearch}"`;
        }
        if (filterInfo) filterInfo.textContent = info;

        // Show/hide no results
        if (visibleCount === 0) {
            if (noResults) noResults.classList.remove('hidden');
            if (projectsContainer) projectsContainer.classList.add('hidden');
        } else {
            if (noResults) noResults.classList.add('hidden');
            if (projectsContainer) projectsContainer.classList.remove('hidden');
        }
    }
});
