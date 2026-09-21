(function () {
  "use strict";

  var GLYPHS = "ABCDEF0123456789#%&*+-=";
  var TOTAL = 24;
  var INTERVAL_MS = 40;

  function scrambleEl(el) {
    var text = el.getAttribute("data-text") || el.textContent || "";
    var frame = 0;
    var id = window.setInterval(function () {
      frame++;
      if (frame >= TOTAL) {
        el.textContent = text;
        window.clearInterval(id);
        return;
      }
      el.textContent = text
        .split("")
        .map(function (ch, i) {
          if (ch === " " || ch === "—" || ch === "–") return ch;
          if (frame + i < TOTAL) {
            return GLYPHS[Math.floor(Math.random() * GLYPHS.length)];
          }
          return text[i];
        })
        .join("");
    }, INTERVAL_MS);
  }

  document.querySelectorAll("[data-scramble]").forEach(scrambleEl);
})();
