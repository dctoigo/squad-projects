function initializeTaskToggles() {
    document.querySelectorAll('[data-bs-toggle="collapse"]').forEach(element => {
        if (element.dataset.initialized) return;
        
        element.dataset.initialized = 'true';
        element.addEventListener('click', function() {
            const icon = this.querySelector('.task-toggle-icon');
            if (!icon) return;
            
            const target = document.querySelector(this.dataset.bsTarget);
            if (!target) return;
            
            target.addEventListener('shown.bs.collapse', () => {
                icon.classList.remove('bi-plus');
                icon.classList.add('bi-dash');
            }, { once: true });
            
            target.addEventListener('hidden.bs.collapse', () => {
                icon.classList.remove('bi-dash');
                icon.classList.add('bi-plus');
            }, { once: true });
        });
    });
}

document.addEventListener('DOMContentLoaded', initializeTaskToggles);
document.body.addEventListener('htmx:afterSwap', initializeTaskToggles);