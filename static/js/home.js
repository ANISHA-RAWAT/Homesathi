document.querySelectorAll('.hs-city-bar-fill').forEach(el => {
  el.style.width = el.dataset.width + '%';
});
// Horizontal scroll arrows
document.querySelectorAll('.h-scroll-wrapper').forEach(function(wrapper) {
    var track = wrapper.querySelector('.h-scroll-track');
    var prev  = wrapper.querySelector('.scroll-prev');
    var next  = wrapper.querySelector('.scroll-next');
    if (prev) prev.addEventListener('click', function() { track.scrollBy({left: -320, behavior: 'smooth'}); });
    if (next) next.addEventListener('click', function() { track.scrollBy({left: 320, behavior: 'smooth'}); });
});

// BHK tabs
document.querySelectorAll('.hs-bhk-tab').forEach(function(tab) {
    tab.addEventListener('click', function() {
        document.querySelectorAll('.hs-bhk-tab').forEach(function(t) { t.classList.remove('active'); });
        document.querySelectorAll('.hs-bhk-panel').forEach(function(p) { p.classList.remove('active'); });
        tab.classList.add('active');
        var panel = document.getElementById(tab.dataset.target);
        if (panel) panel.classList.add('active');
    });
});

// Budget tabs
document.querySelectorAll('.hs-budget-tab').forEach(function(tab) {
    tab.addEventListener('click', function() {
        document.querySelectorAll('.hs-budget-tab').forEach(function(t) { t.classList.remove('active'); });
        document.querySelectorAll('.hs-budget-panel').forEach(function(p) { p.classList.remove('active'); });
        tab.classList.add('active');
        var panel = document.getElementById(tab.dataset.target);
        if (panel) panel.classList.add('active');
    });
});
(function(){
    var track  = document.getElementById('heroTrack');
    var slides = track.querySelectorAll('.hs-slide');
    var dotsEl = document.getElementById('slideDots');
    var prev   = document.getElementById('slidePrev');
    var next   = document.getElementById('slideNext');
    var cur    = 0;
    var timer;

    // Build dots
    slides.forEach(function(_, i) {
        var d = document.createElement('button');
        d.className = 'hs-dot' + (i === 0 ? ' active' : '');
        d.addEventListener('click', function(){ goTo(i); });
        dotsEl.appendChild(d);
    });

    function goTo(n) {
        slides[cur].classList.remove('active');
        dotsEl.children[cur].classList.remove('active');
        cur = (n + slides.length) % slides.length;
        slides[cur].classList.add('active');
        dotsEl.children[cur].classList.add('active');
        track.style.transform = 'translateX(-' + (cur * 100) + '%)';
    }
    slides[0].classList.add('active');
    prev.addEventListener('click', function(){ goTo(cur - 1); resetTimer(); });
    next.addEventListener('click', function(){ goTo(cur + 1); resetTimer(); });
    function resetTimer() { clearInterval(timer); timer = setInterval(function(){ goTo(cur+1); }, 5000); }
    resetTimer();
})();

/* ── Horizontal scroll arrows ────────────── */
document.querySelectorAll('.h-scroll-wrapper').forEach(function(wrapper){
    var track = wrapper.querySelector('.h-scroll-track');
    var p = wrapper.querySelector('.scroll-prev');
    var n = wrapper.querySelector('.scroll-next');
    if(p) p.addEventListener('click', function(){ track.scrollBy({left:-320,behavior:'smooth'}); });
    if(n) n.addEventListener('click', function(){ track.scrollBy({left:320,behavior:'smooth'}); });
});

/* ── BHK tabs ────────────────────────────── */
document.querySelectorAll('.hs-bhk-tab').forEach(function(tab){
    tab.addEventListener('click', function(){
        document.querySelectorAll('.hs-bhk-tab').forEach(function(t){ t.classList.remove('active'); });
        document.querySelectorAll('.hs-bhk-panel').forEach(function(p){ p.classList.remove('active'); });
        tab.classList.add('active');
        var panel = document.getElementById(tab.dataset.target);
        if(panel) panel.classList.add('active');
    });
});

/* ── Budget tabs ─────────────────────────── */
document.querySelectorAll('.hs-budget-tab').forEach(function(tab){
    tab.addEventListener('click', function(){
        document.querySelectorAll('.hs-budget-tab').forEach(function(t){ t.classList.remove('active'); });
        document.querySelectorAll('.hs-budget-panel').forEach(function(p){ p.classList.remove('active'); });
        tab.classList.add('active');
        var panel = document.getElementById(tab.dataset.target);
        if(panel) panel.classList.add('active');
    });
});