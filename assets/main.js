// Progressive enhancement only: the site works fully without this file.
// Respect reduced-motion: stop autoplaying videos and expose native controls.
(function () {
  var mq = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)");
  function apply() {
    var vids = document.querySelectorAll("video[autoplay]");
    for (var i = 0; i < vids.length; i++) {
      if (mq && mq.matches) {
        vids[i].pause();
        vids[i].setAttribute("controls", "");
      } else {
        vids[i].removeAttribute("controls");
        var p = vids[i].play();
        if (p && p.catch) p.catch(function () {});
      }
    }
  }
  if (mq) {
    apply();
    if (mq.addEventListener) mq.addEventListener("change", apply);
  }
})();
