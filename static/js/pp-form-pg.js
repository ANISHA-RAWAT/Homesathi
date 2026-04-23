/**
 * pp-form-pg.js
 * Panels for PG Owner seller type.
 * Depends on: pp-data.js, pp-helpers.js, pp-media.js
 */
'use strict';

var PP_PG = (function () {
  var H = PP_H;
  var D = PP_DATA;

  /* ── PANEL 1: PG BASICS ──────────────────────────────────── */
  function basicsPanel() {
    var html = '';

    html += H.field('PG Name / Title',
      H.textInput('title', 'e.g. Sai PG for Girls, Model Town'),
      '', true);

    html += H.twoCol(
      H.field('Monthly Rent (₹)',
        H.prefixInput('price', 'e.g. 8000', '₹'),
        'Per person / per bed', true),
      H.field('PG For',
        H.chipGroup('pg_for', [
          { key:'male',   label:'Male',   emoji:'👨' },
          { key:'female', label:'Female', emoji:'👩' },
          { key:'any',    label:'Any',    emoji:'👥' },
        ], false))
    );

    html += H.twoCol(
      H.field('City', H.textInput('city', 'e.g. Ludhiana'), '', true),
      H.field('State', H.textInput('state', 'e.g. Punjab'), '')
    );

    html += H.twoCol(
      H.field('Locality', H.textInput('location', 'e.g. Model Town'), ''),
      H.field('Full Address', H.textInput('address', 'House No., Street, Landmark…'), '')
    );

    html += H.field('PG Description',
      H.textarea('description',
        'Describe your PG — room types, house rules, nearby colleges, metro/bus access, food options…', 4),
      '', true);

    html += H.field('Key Facilities',
      H.textInput('key_facilities', 'e.g. 24hr Security, CCTV, Common Kitchen, Study Room'),
      'Comma-separated');

    return { id: 'basics', title: 'Basics', icon: '📝', html: html };
  }

  /* ── PANEL 2: ROOM & OCCUPANCY ───────────────────────────── */
  function roomPanel() {
    var html = '';

    html += H.sectionHead('Room Types Available');
    html += H.field('Room Sharing Type',
      H.chipGroup('room_sharing', [
        { key:'single',  label:'Single Occupancy',  emoji:'🛏️' },
        { key:'double',  label:'Double Sharing',    emoji:'👥' },
        { key:'triple',  label:'Triple Sharing',    emoji:'👨‍👩‍👦' },
        { key:'dormitory', label:'Dormitory',       emoji:'🏨' },
      ], true),
      'Select all room types you offer');

    html += H.twoCol(
      H.field('Total Beds Available', H.numberInput('total_beds', '0', 1), '', true),
      H.field('Beds Currently Available', H.numberInput('available_beds', '0', 0), '')
    );

    html += H.sectionHead('Bathroom');
    html += H.twoCol(
      H.field('Total Bathrooms', H.numberInput('bathrooms', '0', 0), ''),
      H.field('Bathroom Type',
        H.selectInput('bathroom_type', [
          ['','Select'],
          ['attached','Attached / Private (per room)'],
          ['common','Common / Shared'],
          ['both','Mix — Some Attached, Some Common'],
        ]), 'Type of bathroom available for occupants')
    );

    html += H.sectionHead('Pricing & Stay');
    html += H.twoCol(
      H.field('Security Deposit (₹)',
        H.prefixInput('security_deposit', 'e.g. 10000', '₹'), ''),
      H.field('Notice Period',
        H.textInput('pg_notice_period', 'e.g. 30 days or 1 month'), '')
    );
    html += H.twoCol(
      H.field('Min Stay Duration',
        H.selectInput('min_stay', [
          ['','Select'],['1_month','1 Month'],['3_months','3 Months'],
          ['6_months','6 Months'],['1_year','1 Year'],['no_min','No Minimum'],
        ]), ''),
      H.field('Meals Included',
        H.selectInput('meals_included', [
          ['','Select'],['no_meals','No Meals'],['breakfast','Breakfast Only'],
          ['two_meals','Breakfast + Dinner'],['three_meals','3 Meals / Day'],
        ]), '')
    );

    html += H.sectionHead('Rules & Preferences');
    html += H.twoCol(
      H.field('Gate Closing Time',
        H.selectInput('gate_time', [
          ['','Select'],['9pm','9:00 PM'],['10pm','10:00 PM'],
          ['11pm','11:00 PM'],['12am','12:00 AM (Midnight)'],['no_restriction','No Restriction'],
        ]), ''),
      H.field('Visitors Allowed',
        H.selectInput('visitors_allowed', [
          ['','Select'],['yes','Yes'],['no','No'],['limited','Limited Hours'],
        ]), '')
    );

    html += H.field('Vastu Compliant', H.toggleSwitch('vastu_compliant', 'Yes, Vastu compliant'), '');

    return { id: 'room', title: 'Room & Stay', icon: '🏠', html: html };
  }

  /* ── PANEL 3: AMENITIES ──────────────────────────────────── */
  function amenitiesPanel() {
    var html = '';

    html += H.sectionHead('PG Amenities & Facilities');
    html += '<p class="pp-hint-text" style="margin-bottom:12px">Select all amenities available at your PG</p>';
    html += H.field('', H.chipGroup('pg_amenities', D.PG_AMENITIES, true), '');

    html += H.sectionHead('Furnishing in Room');
    html += H.field('', H.chipGroup('room_furnishing', [
      { key:'bed',          label:'Bed',           emoji:'🛏️' },
      { key:'mattress',     label:'Mattress',      emoji:'🛌' },
      { key:'pillow',       label:'Pillow',        emoji:'🛋️' },
      { key:'wardrobe',     label:'Wardrobe',      emoji:'🪞' },
      { key:'study_table',  label:'Study Table',   emoji:'📚' },
      { key:'chair',        label:'Chair',         emoji:'🪑' },
      { key:'fan',          label:'Fan',           emoji:'🌀' },
      { key:'ac',           label:'AC',            emoji:'❄️' },
      { key:'geyser',       label:'Geyser',        emoji:'🔥' },
      { key:'tv',           label:'TV',            emoji:'📺' },
      { key:'fridge',       label:'Mini Fridge',   emoji:'🧊' },
    ], true), 'Items provided inside the room');

    html += H.sectionHead('Common Area Facilities');
    html += H.field('', H.chipGroup('common_areas', [
      { key:'common_kitchen',  label:'Common Kitchen', emoji:'🍳' },
      { key:'dining_area',     label:'Dining Area',    emoji:'🍽️' },
      { key:'tv_lounge',       label:'TV Lounge',      emoji:'📺' },
      { key:'terrace',         label:'Terrace Access', emoji:'🌇' },
      { key:'garden',          label:'Garden',         emoji:'🌳' },
      { key:'indoor_games',    label:'Indoor Games',   emoji:'🎮' },
    ], true), 'Shared spaces available');

    return { id: 'amenities', title: 'Amenities', icon: '✨', html: html };
  }

  /* ── MAIN BUILDER ────────────────────────────────────────── */
  function getPanels() {
    return [
      basicsPanel(),
      roomPanel(),
      amenitiesPanel(),
      PP_MEDIA.mediaPanel(),
    ];
  }

  return { getPanels: getPanels };
})();