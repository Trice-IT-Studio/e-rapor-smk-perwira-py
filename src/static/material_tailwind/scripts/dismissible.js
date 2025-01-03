(function () {
  var dismissible = document.querySelectorAll("[data-dismissible]");
  var targets = document.querySelectorAll("[data-dismissible-target]");
  if (dismissible && targets) {
    dismissible.forEach(function (dismiss) {
      return targets.forEach(function (target) {
        if (dismiss.dataset.dismissible === target.dataset.dismissibleTarget) {
          target.addEventListener("click", function () {
            dismiss.classList.toggle("hidden");
          });
        }
      });
    });
  }
})();
