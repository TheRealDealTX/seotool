/* rooftarp.com — the only script on the site.
   Mobile nav toggle, plus a guard on the callback form so it cannot silently
   swallow an enquiry while it is unwired. See "Known gaps" in README.md. */

(function () {
  "use strict";

  // ---------------------------------------------------------- mobile nav
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });

    // Close the menu when a link is followed or Escape is pressed.
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  // ------------------------------------------------------- callback form
  // The form has no backend yet. Rather than post to nowhere and look like it
  // worked, it tells the visitor to call — an unanswered emergency enquiry is
  // worse than no form at all.
  var form = document.querySelector(".callback-form");
  if (form && form.getAttribute("data-unwired") === "true") {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var note = form.querySelector(".form-status");
      if (!note) {
        note = document.createElement("p");
        note.className = "form-status";
        form.appendChild(note);
      }
      note.textContent =
        "This form is not connected yet — please call (956) 465-6045 so we can help right away.";
      note.setAttribute("role", "alert");
    });
  }
})();
