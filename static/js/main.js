// ============================
// main.js — RentalHome
// ============================

document.addEventListener('DOMContentLoaded', function () {

    // ── USER DROPDOWN (click to open, click outside to close) ──
    const userBtn      = document.querySelector('.nav-user-btn');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    if (userBtn && dropdownMenu) {
        userBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            dropdownMenu.classList.toggle('open');
        });

        document.addEventListener('click', function () {
            dropdownMenu.classList.remove('open');
        });

        dropdownMenu.addEventListener('click', function (e) {
            e.stopPropagation();
        });
    }

    // ── MOBILE MENU ──
    const menuToggle = document.getElementById('menuToggle');
    const mobileNav  = document.getElementById('mobileNav');

    if (menuToggle && mobileNav) {
        menuToggle.addEventListener('click', function () {
            mobileNav.classList.toggle('open');
        });
    }

    // ── AUTO-DISMISS ALERTS after 5 seconds ──
    document.querySelectorAll('.alert').forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(20px)';
            alert.style.transition = 'opacity 0.3s, transform 0.3s';
            setTimeout(function () { alert.remove(); }, 300);
        }, 5000);
    });

    // ── HERO SEARCH — sync listing type from URL ──
    const heroForm = document.querySelector('.hero-search-form');
    if (heroForm) {
        const urlParams = new URLSearchParams(window.location.search);
        const lt = urlParams.get('listing_type');
        if (lt) {
            const sel = heroForm.querySelector('select[name="listing_type"]');
            if (sel) sel.value = lt;
        }
    }

});