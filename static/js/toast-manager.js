class ToastManager {
    constructor() {
        this.containerSelector = '.toast-container';
        this.initContainer();
        this.bindHtmxEvents();
    }

    getBackgroundClass(type) {
        const classes = {
            'success': 'bg-success text-white',
            'danger': 'bg-danger text-white',
            'warning': 'bg-warning text-dark',
            'info': 'bg-info text-white'
        };
        return classes[type] || classes.info;
    }

    initContainer() {
        if (!document.querySelector(this.containerSelector)) {
            const container = document.createElement('div');
            container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(container);
        }
    }

    show(message, type = 'success', title = '') {
        const toastContainer = document.querySelector(this.containerSelector);
        const toast = document.createElement('div');
        
        const bgClass = this.getBackgroundClass(type);
        toast.className = `toast align-items-center border-0 ${bgClass}`;
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${title ? `<strong>${title}</strong><br>` : ''}
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        new bootstrap.Toast(toast, {
            animation: true,
            autohide: true,
            delay: 5000
        }).show();
        
        toast.addEventListener('hidden.bs.toast', () => toast.remove());
    }

    bindHtmxEvents() {
        // HTMX Response Error Handler
        document.body.addEventListener('htmx:responseError', (evt) => {
            const response = evt.detail.xhr.response;
            try {
                const data = JSON.parse(response);
                this.show(data.error, 'danger', data.title || 'Erro');
            } catch (e) {
                this.show('Ocorreu um erro inesperado', 'danger', 'Erro');
            }
        });

        // HTMX After Swap Success Handler
        document.body.addEventListener('htmx:afterSwap', (evt) => {
            const xhr = evt.detail.xhr;
            if (xhr?.status === 200 || xhr?.status === 204) {
                try {
                    const response = JSON.parse(xhr.response || '{}');
                    if (response.taskUpdated) {
                        const projectId = response.taskUpdated.project_id;
                        const panel = document.querySelector(`#task-panel-${projectId}`);
                        if (panel) {
                            panel.dispatchEvent(new Event('reload'));
                        }
                    }
                    if (response.message) {
                        this.show(response.message, response.type || 'success', response.title);
                    }
                } catch (e) {
                    // Ignore non-JSON responses
                }
            }
        });
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    window.toastManager = new ToastManager();
});

// Export para uso global
window.showToast = (message, type, title) => {
    window.toastManager?.show(message, type, title);
};