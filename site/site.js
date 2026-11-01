// UCG brand kit site: copy buttons, filters, icon colorways, lazy video, mobile nav.
(function () {
  // Collapse the guide list on small screens
  var nav = document.querySelector(".nav-details");
  if (nav && window.matchMedia("(max-width: 900px)").matches) nav.removeAttribute("open");

  // Copy-to-clipboard buttons: <button class="copy" data-copy="#1E2B38">
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-copy]");
    if (!b) return;
    var text = b.getAttribute("data-copy");
    var done = function () {
      var old = b.textContent;
      b.textContent = "Copied";
      b.classList.add("is-done");
      setTimeout(function () { b.textContent = old; b.classList.remove("is-done"); }, 1400);
    };
    if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, done); else done();
  });

  // Filter groups: <div data-filter-group="photos"><button data-filter="all|tag">  items: [data-tags]
  document.querySelectorAll("[data-filter-group]").forEach(function (group) {
    var target = document.getElementById(group.getAttribute("data-filter-group"));
    group.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-filter]");
      if (!b) return;
      group.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      var f = b.getAttribute("data-filter");
      target.querySelectorAll("[data-tags]").forEach(function (it) {
        it.hidden = !(f === "all" || it.getAttribute("data-tags").split(" ").indexOf(f) > -1);
      });
    });
  });

  // Swap groups: buttons with data-swap="key" change every [data-swap-<key>] attr in the target
  // e.g. icon colorways (src + tile background) and photo tone (color / bw).
  document.querySelectorAll("[data-swap-group]").forEach(function (group) {
    var target = document.getElementById(group.getAttribute("data-swap-group"));
    group.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-swap]");
      if (!b) return;
      group.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      var k = b.getAttribute("data-swap");
      target.querySelectorAll("[data-src-" + k + "]").forEach(function (img) { img.src = img.getAttribute("data-src-" + k); });
      target.querySelectorAll("[data-href-" + k + "]").forEach(function (a) { a.href = a.getAttribute("data-href-" + k); });
      target.querySelectorAll("[data-class-" + k + "]").forEach(function (el) {
        el.className = el.getAttribute("data-class-" + k);
      });
    });
  });

  // Videos play only while on screen
  var vids = document.querySelectorAll("video[data-autoplay]");
  if ("IntersectionObserver" in window && vids.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var v = en.target;
        if (en.isIntersecting) { v.play().catch(function () {}); } else { v.pause(); }
      });
    }, { threshold: 0.4 });
    vids.forEach(function (v) { io.observe(v); });
  }
})();
