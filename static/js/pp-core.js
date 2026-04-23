/**
 * pp-core.js
 * Core form engine: state, screen navigation, panel rendering,
 * step navigation, progress bar, and field validation.
 * Depends on: pp-data.js, pp-helpers.js, pp-media.js,
 *             pp-form-owner.js, pp-form-builder.js, pp-form-pg.js
 */
'use strict';

var PP_CORE = (function () {
  var D = PP_DATA;

  /* ── STATE ───────────────────────────────────────────────── */
  var state = {
    sellerType:   '',
    category:     '',
    propertyType: '',
    step:         0,
    totalSteps:   0,
  };

  /* ── SCREEN MANAGEMENT ───────────────────────────────────── */
  var SCREEN_IDS = ['screen-seller', 'screen-category', 'screen-subtype', 'formWrap'];

  function showScreen(id) {
    SCREEN_IDS.forEach(function (sid) {
      var el = document.getElementById(sid);
      if (!el) return;
      if (sid === id) el.classList.remove('hidden');
      else el.classList.add('hidden');
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  /* ── PANEL SELECTION ─────────────────────────────────────── */
  function getPanels() {
    var s = state.sellerType, cat = state.category, pt = state.propertyType;
    if (s === 'pg_owner') return PP_PG.getPanels();
    if (s === 'builder')  return PP_BUILDER.getPanels(cat, pt);
    return PP_OWNER.getPanels(cat, pt);
  }

  /* ── BUILD & SHOW FORM ───────────────────────────────────── */
  function buildAndShowForm() {
    var panels = getPanels();
    state.totalSteps = panels.length;
    state.step = 0;

    _buildStepNav(panels);
    _buildBreadcrumb();
    _buildPanels(panels);

    PP_MEDIA.initImageUpload();
    _initFurnishingToggle();
    _initListingTypeSync();

    showScreen('formWrap');
    _updateNavAndProgress();
  }

  /* ── STEP NAV ────────────────────────────────────────────── */
  function _buildStepNav(panels) {
    var nav = document.getElementById('ppStepsNav');
    nav.innerHTML = '';
    panels.forEach(function (panel, i) {
      if (i > 0) {
        var conn = document.createElement('div');
        conn.className = 'pp-step-conn';
        nav.appendChild(conn);
      }
      var pill = document.createElement('button');
      pill.type = 'button';
      pill.className = 'pp-step-pill' + (i === 0 ? ' active' : '');
      pill.dataset.step = i;
      pill.innerHTML =
        '<span class="pp-step-num">' + (i + 1) + '</span>' +
        '<span class="pp-step-icon">' + panel.icon + '</span>' +
        '<span class="pp-step-lbl">' + panel.title + '</span>';
      pill.addEventListener('click', function () {
        var t = parseInt(this.dataset.step, 10);
        if (t < state.step) goToStep(t);
      });
      nav.appendChild(pill);
    });
  }

  /* ── BREADCRUMB ──────────────────────────────────────────── */
  function _buildBreadcrumb() {
    var sellerLabels = { pg_owner: 'PG Owner', owner: 'Owner', builder: 'Builder', dealer: 'Dealer / Agent' };
    var catLabels    = { residential: 'Residential', commercial: 'Commercial', pg: 'PG' };

    var subtypeLabel = '';
    var allSubs = D.RESIDENTIAL_SUBTYPES.concat(D.COMMERCIAL_SUBTYPES);
    for (var i = 0; i < allSubs.length; i++) {
      if (allSubs[i].value === state.propertyType) { subtypeLabel = allSubs[i].label; break; }
    }

    var bc = document.getElementById('ppBreadcrumb');
    bc.innerHTML =
      '<span class="bc-item">' + (sellerLabels[state.sellerType] || '') + '</span>' +
      (state.category && state.category !== 'pg'
        ? '<span class="bc-sep">›</span><span class="bc-item">' + (catLabels[state.category] || '') + '</span>'
        : '') +
      (subtypeLabel
        ? '<span class="bc-sep">›</span><span class="bc-item bc-active">' + subtypeLabel + '</span>'
        : '') +
      '<button type="button" class="bc-change" id="bcChange">Change</button>';

    var bcChange = document.getElementById('bcChange');
    if (bcChange) {
      bcChange.addEventListener('click', function () {
        if (state.sellerType === 'pg_owner') showScreen('screen-seller');
        else showScreen('screen-subtype');
      });
    }
  }

  /* ── PANELS ──────────────────────────────────────────────── */
  function _buildPanels(panels) {
    var body = document.getElementById('ppFormBody');
    body.innerHTML = '';
    panels.forEach(function (panel, i) {
      var div = document.createElement('div');
      div.className = 'pp-panel' + (i === 0 ? ' active' : '');
      div.id = 'pp-panel-' + i;
      div.innerHTML =
        '<div class="pp-panel-header">' +
          '<span class="pp-panel-icon">' + panel.icon + '</span>' +
          '<div><h2 class="pp-panel-title">' + panel.title + '</h2></div>' +
        '</div>' +
        '<div class="pp-panel-content">' + panel.html + '</div>';
      body.appendChild(div);
    });
  }

  /* ── STEP NAVIGATION ─────────────────────────────────────── */
  function goToStep(n) {
    var oldPanel = document.getElementById('pp-panel-' + state.step);
    var newPanel = document.getElementById('pp-panel-' + n);
    if (oldPanel) oldPanel.classList.remove('active');
    if (newPanel) newPanel.classList.add('active');
    state.step = n;
    _updateNavAndProgress();
    var body = document.getElementById('ppFormBody');
    if (body) body.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function _updateNavAndProgress() {
    var pct = state.totalSteps > 1 ? (state.step / (state.totalSteps - 1)) * 100 : 100;
    var fill = document.getElementById('ppProgressFill');
    if (fill) fill.style.width = pct + '%';

    document.querySelectorAll('.pp-step-pill').forEach(function (pill) {
      var s = parseInt(pill.dataset.step, 10);
      pill.classList.toggle('active',    s === state.step);
      pill.classList.toggle('completed', s < state.step);
    });

    var isLast = state.step === state.totalSteps - 1;
    var btnBack   = document.getElementById('ppBtnBack');
    var btnNext   = document.getElementById('ppBtnNext');
    var btnSubmit = document.getElementById('ppBtnSubmit');

    if (btnBack)   btnBack.style.display = state.step === 0 ? 'none' : '';
    if (btnNext)   btnNext.classList.toggle('hidden', isLast);
    if (btnSubmit) btnSubmit.classList.toggle('hidden', !isLast);
  }

  /* ── VALIDATION ──────────────────────────────────────────── */
  function validateCurrentPanel() {
    var panel = document.getElementById('pp-panel-' + state.step);
    if (!panel) return true;
    var ok = true;

    // Required text/number/select inputs
    panel.querySelectorAll('.pp-input[name]').forEach(function (el) {
      var fb  = el.closest('.pp-field');
      var lbl = fb && fb.querySelector('.pp-label');
      if (!lbl || !lbl.querySelector('.req-star')) return;
      var val = (el.value || '').trim();
      if (!val) {
        ok = false;
        el.classList.add('input-error');
        el.addEventListener('input', function () { el.classList.remove('input-error'); }, { once: true });
      }
    });

    // Required radio groups (listing type)
    panel.querySelectorAll('.listing-type-group').forEach(function (grp) {
      if (!grp.querySelector('input:checked')) {
        ok = false;
        grp.classList.add('group-error');
        grp.addEventListener('change', function () { grp.classList.remove('group-error'); }, { once: true });
      }
    });

    if (!ok) {
      var firstErr = panel.querySelector('.pp-input.input-error');
      if (firstErr) firstErr.focus();
    }
    return ok;
  }

  /* ── LISTING TYPE SYNC ───────────────────────────────────── */
  function _initListingTypeSync() {
    document.querySelectorAll('[name="listing_type_choice"]').forEach(function (radio) {
      radio.addEventListener('change', function () {
        var hlt = document.getElementById('hListingType');
        if (hlt) hlt.value = this.value;
      });
    });
    var checked = document.querySelector('[name="listing_type_choice"]:checked');
    if (!checked) {
      var first = document.querySelector('[name="listing_type_choice"]');
      if (first) {
        first.checked = true;
        var hlt = document.getElementById('hListingType');
        if (hlt) hlt.value = first.value;
      }
    }
  }

  /* ── FURNISHING TOGGLE ───────────────────────────────────── */
  function _initFurnishingToggle() {
    document.querySelectorAll('[name="furnishing_status"]').forEach(function (radio) {
      radio.addEventListener('change', function () {
        var sec = document.getElementById('furnItemsSection');
        if (sec) sec.style.display = this.value === 'unfurnished' ? 'none' : '';
      });
    });
  }

  /* ── PUBLIC API ──────────────────────────────────────────── */
  return {
    state:            state,
    showScreen:       showScreen,
    buildAndShowForm: buildAndShowForm,
    goToStep:         goToStep,
    validateCurrentPanel: validateCurrentPanel,
  };
})();