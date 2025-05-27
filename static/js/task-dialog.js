document.addEventListener("DOMContentLoaded", function () {
    const modalEl = document.getElementById("modal");
    const dialogEl = document.getElementById("dialog");
    const bsModal = new bootstrap.Modal(modalEl);

    // Handle HTMX after swap
    htmx.on("htmx:afterSwap", (e) => {
        if (e.detail.target.id === "dialog") {
            bsModal.show();
        }
    });

    // Handle HTMX before swap
    htmx.on("htmx:beforeSwap", (e) => {
        // For 204 responses, prevent content swap
        if (e.detail.target.id === "dialog" && e.detail.xhr.status === 204) {
            e.detail.shouldSwap = false;
        }
    });

    // Handle modal hidden event
    modalEl.addEventListener("hidden.bs.modal", () => {
        // Only clear dialog if it exists
        if (dialogEl) {
            dialogEl.innerHTML = "";
        }
    });

    // Handle task updates
    htmx.on("htmx:afterSettle", (e) => {
        if (e.detail.xhr && e.detail.xhr.status === 204) {
            const triggerHeader = e.detail.xhr.getResponseHeader("HX-Trigger");
            if (triggerHeader) {
                try {
                    const triggers = JSON.parse(triggerHeader);
                    if (triggers.closeModal) {
                        bsModal.hide();
                    }
                } catch (err) {
                    console.warn("Error parsing HX-Trigger:", err);
                }
            }
        }
    });
});