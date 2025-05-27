document.addEventListener("DOMContentLoaded", function () {
      const modalEl = document.getElementById("modal");
      const bsModal = new bootstrap.Modal(modalEl);

      htmx.on("htmx:afterSwap", (e) => {
        if (e.detail.target.id === "dialog") {
          bsModal.show();
        }
      });

      htmx.on("htmx:beforeSwap", (e) => {
        if (e.detail.target.id === "dialog" && !e.detail.xhr.response) {
          bsModal.hide();
          e.detail.shouldSwap = false;
        }
      });

      htmx.on("htmx:beforeRequest", (e) => {
        const dialog = document.getElementById("dialog");
        if (dialog && dialog.innerHTML.trim() === "") {
          dialog.innerHTML = `
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">Carregando...</h5>
              </div>
              <div class="modal-body text-center py-5">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </div>
            </div>
          `;
        }
      });

      document.body.addEventListener("htmx:closeModal", () => {
        bsModal.hide();
      });

      modalEl.addEventListener("hidden.bs.modal", () => {
        document.getElementById("dialog").innerHTML = "";
      });
    });
