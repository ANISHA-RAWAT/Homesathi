/**
 * pp-helpers.js
 * Reusable HTML builder functions for form fields, chips, toggles, etc.
 * Depends on: pp-data.js
 */
'use strict';

var PP_H = (function () {

  function esc(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  /* ── FIELD WRAPPER ───────────────────────────────────────── */
  function field(label, input, hint, required, optional) {
    var reqMark  = required ? '<span class="req-star">*</span>' : '';
    var optTag   = optional ? '<span class="opt-tag">optional</span>' : '';
    var hintHtml = hint ? '<p class="field-hint">' + hint + '</p>' : '';
    return '<div class="pp-field"><label class="pp-label">' + label + reqMark + optTag + '</label>' + input + hintHtml + '</div>';
  }

  /* ── INPUT TYPES ─────────────────────────────────────────── */
  function textInput(name, placeholder, extra) {
    return '<input type="text" name="' + esc(name) + '" placeholder="' + esc(placeholder) + '" class="pp-input"' + (extra||'') + '>';
  }

  function numberInput(name, placeholder, min, extra) {
    var minAttr = (min !== undefined && min !== null) ? ' min="' + min + '"' : '';
    return '<input type="number" name="' + esc(name) + '" placeholder="' + esc(placeholder) + '" class="pp-input"' + minAttr + (extra||'') + '>';
  }

  function selectInput(name, options) {
    var opts = options.map(function(o){
      return '<option value="' + esc(o[0]) + '">' + esc(o[1]) + '</option>';
    }).join('');
    return '<select name="' + esc(name) + '" class="pp-input pp-select">' + opts + '</select>';
  }

  function textarea(name, placeholder, rows) {
    return '<textarea name="' + esc(name) + '" placeholder="' + esc(placeholder) + '" class="pp-input pp-textarea" rows="' + (rows||4) + '"></textarea>';
  }

  function prefixInput(name, placeholder, prefix, min) {
    var minAttr = (min !== undefined) ? ' min="' + min + '"' : '';
    return '<div class="input-pfx"><span>' + prefix + '</span><input type="number" name="' + esc(name) + '" placeholder="' + esc(placeholder) + '" class="pp-input"' + minAttr + '></div>';
  }

  /* ── TOGGLE ──────────────────────────────────────────────── */
  function toggleSwitch(name, label) {
    return '<label class="pp-toggle"><input type="checkbox" name="' + esc(name) + '" class="pp-toggle-input"><span class="pp-toggle-track"><span class="pp-toggle-thumb"></span></span><span class="pp-toggle-label">' + label + '</span></label>';
  }

  /* ── CHIP GROUP ──────────────────────────────────────────── */
  function chipGroup(name, items, multi) {
    var type = multi ? 'checkbox' : 'radio';
    var chips = items.map(function(item){
      return '<label class="pp-chip">' +
        '<input type="' + type + '" name="' + esc(name) + '" value="' + esc(item.key) + '" class="pp-chip-input">' +
        '<span class="pp-chip-emoji">' + item.emoji + '</span>' +
        '<span class="pp-chip-label">' + item.label + '</span>' +
        '</label>';
    }).join('');
    return '<div class="pp-chip-group">' + chips + '</div>';
  }

  /* ── LISTING TYPE BLOCK ──────────────────────────────────── */
  function listingTypeBlock(withPg) {
    var opts = [
      { val:'rent', icon:'🔑', label:'For Rent',      sub:'Monthly rent' },
      { val:'sell', icon:'🏷️', label:'For Sale',      sub:'One-time sale' },
    ];
    if (withPg) opts.push({ val:'pg', icon:'🛏️', label:'PG / Co-living', sub:'Per bed / room' });
    var cards = opts.map(function(o){
      return '<label class="listing-type-card">' +
        '<input type="radio" name="listing_type_choice" value="' + o.val + '">' +
        '<span class="ltc-icon">' + o.icon + '</span>' +
        '<span class="ltc-label">' + o.label + '</span>' +
        '<span class="ltc-sub">' + o.sub + '</span>' +
        '</label>';
    }).join('');
    return '<div class="pp-field field-full"><label class="pp-label">Listing Type<span class="req-star">*</span></label><div class="listing-type-group">' + cards + '</div></div>';
  }

  /* ── LAYOUT HELPERS ──────────────────────────────────────── */
  function twoCol(a, b)      { return '<div class="pp-two-col">'   + a + b      + '</div>'; }
  function threeCol(a, b, c) { return '<div class="pp-three-col">' + a + b + c  + '</div>'; }
  function sectionHead(t)    { return '<div class="pp-section-head">' + t + '</div>'; }

  /* ── BATHROOM FIELDS ─────────────────────────────────────── */
  function bathroomFields(isCommercial) {
    if (isCommercial) {
      return twoCol(
        field('Bathrooms / Washrooms', numberInput('bathrooms', '0', 0), ''),
        field('Bathroom Type', selectInput('bathroom_type', [
          ['','Select'],['attached','Attached'],['common','Common'],['both','Both'],
        ]), '')
      );
    }
    return twoCol(
      field('Bathrooms', numberInput('bathrooms', '0', 0), ''),
      field('Bathroom Type', selectInput('bathroom_type', [
        ['','Select'],['attached','Attached (En-suite)'],['separate','Separate'],
        ['common','Common'],['both_attached_sep','Both Attached & Separate'],
      ]), '')
    );
  }

  /* ── BHK SELECT ──────────────────────────────────────────── */
  function bhkSelect() {
    return selectInput('bhk', [
      ['','Select'],['1rk','1 RK'],['1bhk','1 BHK'],['2bhk','2 BHK'],
      ['3bhk','3 BHK'],['4bhk','4 BHK'],['5bhk+','5 BHK+'],
    ]);
  }

  /* ── FACING SELECT ───────────────────────────────────────── */
  function facingSelect() {
    return selectInput('facing', [
      ['','Select'],['east','East'],['west','West'],['north','North'],['south','South'],
      ['north_east','North-East'],['north_west','North-West'],
      ['south_east','South-East'],['south_west','South-West'],
    ]);
  }

  /* ── FLOORING SELECT ─────────────────────────────────────── */
  function flooringSelect() {
    return selectInput('flooring', [
      ['','Select'],['marble','Marble'],['vitrified_tiles','Vitrified Tiles'],
      ['ceramic_tiles','Ceramic Tiles'],['wooden','Wooden'],
      ['granite','Granite'],['mosaic','Mosaic'],['normal_tiles','Normal Tiles'],
    ]);
  }

  /* ── CONSTRUCTION STATUS ─────────────────────────────────── */
  function constructionStatusSelect() {
    return selectInput('construction_status', [
      ['','Select'],['new_launch','New Launch'],
      ['under_construction','Under Construction'],['ready_to_move','Ready To Move'],
    ]);
  }

  /* ── PROPERTY AGE ────────────────────────────────────────── */
  function propertyAgeSelect() {
    return selectInput('property_age', [
      ['','Select'],['0-1','0-1 Years'],['1-5','1-5 Years'],
      ['5-10','5-10 Years'],['10-20','10-20 Years'],['20+','20+ Years'],
    ]);
  }

  /* ── COMMON LOCATION FIELDS ──────────────────────────────── */
  function locationFields() {
    return twoCol(
      field('City', textInput('city', 'e.g. Ludhiana'), '', true),
      field('State', textInput('state', 'e.g. Punjab'), '')
    ) +
    twoCol(
      field('Locality / Area', textInput('location', 'e.g. Model Town'), ''),
      field('Full Address', textInput('address', 'House No., Street, Society…'), '')
    );
  }

  /* ── OVERLOOKING CHIPS ───────────────────────────────────── */
  function overlookingField() {
    return field('Overlooking', chipGroup('overlooking', PP_DATA.OVERLOOKING, true), 'Select all that apply');
  }

  return {
    field:                   field,
    textInput:               textInput,
    numberInput:             numberInput,
    selectInput:             selectInput,
    textarea:                textarea,
    prefixInput:             prefixInput,
    toggleSwitch:            toggleSwitch,
    chipGroup:               chipGroup,
    listingTypeBlock:        listingTypeBlock,
    twoCol:                  twoCol,
    threeCol:                threeCol,
    sectionHead:             sectionHead,
    bathroomFields:          bathroomFields,
    bhkSelect:               bhkSelect,
    facingSelect:            facingSelect,
    flooringSelect:          flooringSelect,
    constructionStatusSelect: constructionStatusSelect,
    propertyAgeSelect:       propertyAgeSelect,
    locationFields:          locationFields,
    overlookingField:        overlookingField,
  };
})();