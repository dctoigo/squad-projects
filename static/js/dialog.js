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

      document.body.addEventListener("htmx:closeModal", () => {
        bsModal.hide();
      });

      modalEl.addEventListener("hidden.bs.modal", () => {
        document.getElementById("dialog").innerHTML = "";
      });
    });
