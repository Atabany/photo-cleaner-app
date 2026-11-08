// Photo Cleaner site: progressive enhancement only. Every page works without this file.
// 1. Hero preview video: the poster image is the page's main image; the video is fetched only
//    after the page has loaded and the phone is on screen. Reduced motion or Save-Data keeps the
//    poster (the button still lets people play it). Visible pause control (WCAG 2.2.2).
// 2. Sticky download bar on small screens, shown once the hero has scrolled away. Dismissible.
(function () {
  "use strict";
  var doc = document.documentElement;
  var hasIO = "IntersectionObserver" in window;
  var reduceMotion = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : { matches: false };
  var conn = navigator.connection || {};
  var lowData = conn.saveData === true || /(^|-)2g$/.test(conn.effectiveType || "");
  var loaded = document.readyState === "complete";

  function initVideo(box) {
    var src = box.getAttribute("data-video");
    var screen = box.querySelector(".phone-screen");
    var btn = box.parentNode.querySelector(".vid-toggle");
    if (!src || !screen || !btn) return;
    var video = null, userPaused = false, inView = !hasIO;

    function setState(playing) {
      btn.classList.toggle("is-paused", !playing);
      btn.querySelector(".vid-label").textContent = playing ? "Pause preview" : "Play preview";
    }
    function attach() {
      if (video) return;
      video = document.createElement("video");
      video.muted = true;
      video.defaultMuted = true;
      video.loop = true;
      video.playsInline = true;
      video.setAttribute("muted", "");
      video.setAttribute("playsinline", "");
      video.setAttribute("aria-hidden", "true");
      video.setAttribute("tabindex", "-1");
      video.preload = "auto";
      video.className = "phone-video";
      video.addEventListener("playing", function () { box.classList.add("has-video"); setState(true); });
      video.addEventListener("pause", function () { setState(false); });
      video.src = src;
      screen.appendChild(video);
    }
    function play() {
      attach();
      var p = video.play();
      if (p && p.catch) p.catch(function () { setState(false); });
    }
    function detach() {
      // Stop any download in flight so the page can enter the back/forward cache.
      if (!video) return;
      video.pause();
      video.removeAttribute("src");
      video.load();
      screen.removeChild(video);
      video = null;
      box.classList.remove("has-video");
      setState(false);
    }
    function autoplayAllowed() { return !reduceMotion.matches && !lowData && !userPaused; }
    function maybeStart() { if (loaded && inView && autoplayAllowed()) play(); }

    btn.hidden = false;
    setState(false);
    btn.addEventListener("click", function () {
      if (video && !video.paused) { userPaused = true; video.pause(); }
      else { userPaused = false; play(); }
    });
    if (hasIO) {
      new IntersectionObserver(function (entries) {
        inView = entries[0].isIntersecting;
        if (!inView) { if (video && !video.paused) video.pause(); }
        else if (video && !userPaused && (autoplayAllowed() || video.currentTime > 0)) play();
        else maybeStart();
      }, { threshold: 0.2 }).observe(box);
    }
    window.addEventListener("load", function () { loaded = true; setTimeout(maybeStart, 300); });
    if (reduceMotion.addEventListener) {
      reduceMotion.addEventListener("change", function () { if (reduceMotion.matches && video) video.pause(); else maybeStart(); });
    }
    window.addEventListener("pagehide", detach);
    window.addEventListener("pageshow", function (e) { if (e.persisted) maybeStart(); });
    if (loaded) maybeStart();
  }

  function initSticky(bar) {
    var KEY = "pc-download-bar-hidden";
    try { if (sessionStorage.getItem(KEY) === "1") { bar.hidden = true; return; } } catch (e) {}
    var trigger = document.querySelector(".hero") || document.querySelector("main h1");
    if (!hasIO || !trigger) return;
    var close = bar.querySelector(".sticky-close");
    var ctas = document.querySelectorAll("main .store-cta, .site-footer .store-badge-sm");
    var past = false, visible = [];
    function update() {
      var anyVisible = false;
      for (var i = 0; i < visible.length; i++) if (visible[i]) anyVisible = true;
      bar.classList.toggle("is-shown", past && !anyVisible);
    }
    doc.classList.add("sticky-on");
    new IntersectionObserver(function (entries) {
      var e = entries[0];
      past = !e.isIntersecting && e.boundingClientRect.top < 0;
      update();
    }).observe(trigger);
    if (ctas.length) {
      var io = new IntersectionObserver(function (entries) {
        for (var i = 0; i < entries.length; i++) {
          for (var j = 0; j < ctas.length; j++) if (ctas[j] === entries[i].target) visible[j] = entries[i].isIntersecting;
        }
        update();
      });
      for (var k = 0; k < ctas.length; k++) io.observe(ctas[k]);
    }
    if (close) {
      close.hidden = false;
      close.addEventListener("click", function () {
        bar.classList.remove("is-shown");
        bar.hidden = true;
        doc.classList.remove("sticky-on");
        try { sessionStorage.setItem(KEY, "1"); } catch (e) {}
      });
    }
  }

  var boxes = document.querySelectorAll("[data-video]");
  for (var i = 0; i < boxes.length; i++) initVideo(boxes[i]);
  var bar = document.querySelector(".sticky-cta");
  if (bar) initSticky(bar);
})();
