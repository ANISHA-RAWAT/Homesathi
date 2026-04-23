/**
 * pp-init.js
 * Entry point. Wires all event listeners and restores form on POST error.
 * Load ORDER in HTML:
 *   1. pp-data.js
 *   2. pp-helpers.js
 *   3. pp-media.js
 *   4. pp-form-owner.js
 *   5. pp-form-builder.js
 *   6. pp-form-pg.js
 *   7. pp-core.js
 *   8. pp-init.js   ← this file (last)
 */
(function () {
  'use strict';

  var D    = PP_DATA;
  var CORE = PP_CORE;

  /* ── DJANGO ERROR / DATA RESTORE ─────────────────────────── */
  function readJsonScript(id) {
    var el = document.getElementById(id);
    if (!el) return {};
    try {
      var parsed = JSON.parse(el.textContent || el.innerText || '{}');
      return typeof parsed === 'string' ? JSON.parse(parsed) : parsed;
    } catch (e) { return {}; }
  }

  var DJANGO_ERRORS = readJsonScript('django-form-errors');
  var DJANGO_DATA   = readJsonScript('django-form-data');

  /* ── SELLER CARD CLICKS ──────────────────────────────────── */
  document.querySelectorAll('.seller-card').forEach(function (card) {
    card.addEventListener('click', function () {
      CORE.state.sellerType = this.dataset.seller;
      var hSeller = document.getElementById('hSellerType');
      if (hSeller) hSeller.value = CORE.state.sellerType;

      if (CORE.state.sellerType === 'pg_owner') {
        CORE.state.category     = 'pg';
        CORE.state.propertyType = 'pg_hostel';
        _setHidden('hCategory',     'pg');
        _setHidden('hPropertyType', 'pg_hostel');
        _setHidden('hListingType',  'pg');
        CORE.buildAndShowForm();
      } else {
        var eyebrow = { owner: 'Owner', builder: 'Builder', dealer: 'Dealer / Agent' };
        var el = document.getElementById('catEyebrow');
        if (el) el.textContent = eyebrow[CORE.state.sellerType] || '';
        CORE.showScreen('screen-category');
      }
    });
  });

  /* ── CATEGORY CARD CLICKS ────────────────────────────────── */
  document.querySelectorAll('.cat-card').forEach(function (card) {
    card.addEventListener('click', function () {
      CORE.state.category = this.dataset.cat;
      _setHidden('hCategory', CORE.state.category);

      var subtypes = CORE.state.category === 'commercial'
        ? D.COMMERCIAL_SUBTYPES : D.RESIDENTIAL_SUBTYPES;

      var eyebrow = document.getElementById('subtypeEyebrow');
      if (eyebrow) eyebrow.textContent = CORE.state.category === 'commercial' ? 'Commercial' : 'Residential';

      var grid = document.getElementById('subtypeGrid');
      grid.innerHTML = '';
      subtypes.forEach(function (st) {
        var btn = document.createElement('button');
        btn.type      = 'button';
        btn.className = 'subtype-card';
        btn.dataset.value = st.value;
        btn.innerHTML =
          '<span class="stc-emoji">' + st.emoji + '</span>' +
          '<span class="stc-label">' + st.label + '</span>';
        btn.addEventListener('click', function () {
          CORE.state.propertyType = this.dataset.value;
          _setHidden('hPropertyType', CORE.state.propertyType);
          CORE.buildAndShowForm();
        });
        grid.appendChild(btn);
      });

      CORE.showScreen('screen-subtype');
    });
  });

  /* ── BACK BUTTONS ────────────────────────────────────────── */
  var backToSeller = document.getElementById('backToSeller');
  if (backToSeller) backToSeller.addEventListener('click', function () { CORE.showScreen('screen-seller'); });

  var backToCategory = document.getElementById('backToCategory');
  if (backToCategory) backToCategory.addEventListener('click', function () { CORE.showScreen('screen-category'); });

  /* ── FORM NAV BUTTONS ────────────────────────────────────── */
  var btnNext = document.getElementById('ppBtnNext');
  if (btnNext) {
    btnNext.addEventListener('click', function () {
      if (CORE.validateCurrentPanel()) CORE.goToStep(CORE.state.step + 1);
    });
  }

  var btnBack = document.getElementById('ppBtnBack');
  if (btnBack) {
    btnBack.style.display = 'none'; // hide on initial load
    btnBack.addEventListener('click', function () {
      if (CORE.state.step > 0) {
        CORE.goToStep(CORE.state.step - 1);
      } else {
        if (CORE.state.sellerType === 'pg_owner') CORE.showScreen('screen-seller');
        else CORE.showScreen('screen-subtype');
      }
    });
  }

  /* ── RESTORE ON POST ERROR ───────────────────────────────── */
  (function restoreOnError() {
    var sellerType   = _getHidden('hSellerType');
    var category     = _getHidden('hCategory');
    var propertyType = _getHidden('hPropertyType');
    if (!sellerType || !propertyType) return;

    CORE.state.sellerType   = sellerType;
    CORE.state.category     = category;
    CORE.state.propertyType = propertyType;
    CORE.buildAndShowForm();

    // Restore field values from Django POST data
    Object.keys(DJANGO_DATA).forEach(function (name) {
      var val = DJANGO_DATA[name];
      if (!val) return;
      var el = document.querySelector('[name="' + name + '"]');
      if (el && el.type !== 'file') el.value = val;
    });

    // Mark errored fields
    Object.keys(DJANGO_ERRORS).forEach(function (name) {
      var el = document.querySelector('[name="' + name + '"]');
      if (el) el.classList.add('input-error');
    });
  })();

  /* ── HELPERS ─────────────────────────────────────────────── */
  function _setHidden(id, val) {
    var el = document.getElementById(id);
    if (el) el.value = val;
  }

  function _getHidden(id) {
    var el = document.getElementById(id);
    return el ? el.value : '';
  }

})();