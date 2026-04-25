/**
 * pp-form-owner.js
 * Panels for Owner and Dealer / Agent seller types.
 * Depends on: pp-data.js, pp-helpers.js, pp-media.js
 */
'use strict';

var PP_OWNER = (function () {
  var H = PP_H;
  var D = PP_DATA;

  /* ── PLOT SPECIFIC FIELDS (shared between owner & dealer) ─── */
  function plotSpecificFields() {
    var html = '';

    html += H.sectionHead('What Type of Plot?');
    html += H.field('Plot Type',
      H.chipGroup('plot_type', [
        { key: 'residential_plot',  label: 'Residential Plot',   emoji: '🏠' },
        { key: 'commercial_plot',   label: 'Commercial Plot',    emoji: '🏢' },
        { key: 'agricultural_land', label: 'Agricultural Land',  emoji: '🌾' },
        { key: 'industrial_land',   label: 'Industrial Land',    emoji: '🏭' },
      ], false),
      'Select the type of plot you are selling', true);

    html += H.sectionHead('Plot Dimensions');
    html += H.twoCol(
      H.field('Plot Length', H.textInput('plot_length', 'e.g. 20 ft or 6 m'), ''),
      H.field('Plot Width',  H.textInput('plot_width',  'e.g. 10 ft or 3 m'), '')
    );
    html += H.threeCol(
      H.field('Plot Area', H.numberInput('plot_area', 'e.g. 200'), '', true),
      H.field('Unit', H.selectInput('area_unit', D.AREA_UNIT_OPTIONS), '', true),
      H.field('Facing', H.selectInput('facing', D.PLOT_FACING_OPTIONS), '')
    );
    html += H.twoCol(
      H.field('Width of Facing Road',
        H.selectInput('width_of_facing_road', D.ROAD_FACING_OPTIONS),
        'Wider road = higher value'),
      H.field('Open Sides',
        H.selectInput('open_sides', [
          ['','Select'],['1','1 Side'],['2','2 Sides'],['3','3 Sides'],['4','4 Sides (Corner)'],
        ]), '')
    );

    html += H.sectionHead('Utilities Available');
    html += H.field('',
      H.chipGroup('utilities', [
        { key: 'electricity',      label: 'Electricity Available', emoji: '⚡' },
        { key: 'water_connection', label: 'Water Connection',      emoji: '💧' },
        { key: 'sewer_connection', label: 'Sewer Connection',      emoji: '🚰' },
        { key: 'borewell',         label: 'Borewell',              emoji: '🔩' },
      ], true),
      'Select all utilities available at this plot');

    html += H.sectionHead('Legal Status');
    html += H.field('',
      H.chipGroup('legal_status', [
        { key: 'clear_title',    label: 'Clear Title',       emoji: '📄' },
        { key: 'loan_approved',  label: 'Loan Approved',     emoji: '🏦' },
        { key: 'registry_ready', label: 'Registry Ready',    emoji: '✅' },
      ], true),
      'Select all that apply');

    html += H.twoCol(
      H.field('Approved for Construction',
        H.selectInput('approved_for_construction', [
          ['','Select'],['yes','Yes'],['no','No'],
        ]), ''),
      H.field('Property Ownership',
        H.selectInput('property_ownership', [
          ['','Select'],['freehold','Freehold'],['leasehold','Leasehold'],
          ['power_of_attorney','Power of Attorney'],
        ]), '')
    );

    html += H.field('Vastu Compliant', H.toggleSwitch('vastu_compliant', 'Yes, this plot is Vastu compliant'), '');

    return html;
  }

  /* ── PANEL 1: BASICS ─────────────────────────────────────── */
  function basicsPanel(isPlot, isCommercial) {
    var html = H.listingTypeBlock(false);

    html += H.field('Property Title',
      H.textInput('title', isPlot
        ? 'e.g. 200 Sq Yard Residential Plot, Model Town'
        : 'e.g. Spacious 3BHK near Metro, Ludhiana'),
      '', true);

    html += H.twoCol(
      H.field('Price (₹)',
        H.prefixInput('price', isPlot ? 'e.g. 2500000' : 'e.g. 15000', '₹'),
        isPlot ? 'Total plot price' : 'Rent/month or sale price', true),
      H.field('City', H.textInput('city', 'e.g. Ludhiana'), '', true)
    );

    html += H.twoCol(
      H.field('State', H.textInput('state', 'e.g. Punjab'), ''),
      H.field('Locality / Area', H.textInput('location', 'e.g. Model Town'), '')
    );

    html += H.field('Full Address',
      H.textInput('address', 'House No., Street, Society, Landmark…'), '');

    html += H.field('Description',
      H.textarea('description',
        isPlot
          ? 'Describe the plot — shape, surroundings, access road, nearby landmarks…'
          : 'Describe the property, nearby landmarks, transport access…', 4),
      '', true);

    if (!isPlot) {
      html += H.field('Key Highlights',
        H.textarea('key_highlights', 'Why should someone consider this? e.g. Corner unit, park-facing, recently renovated…', 3),
        'Selling points that make your property stand out');
    }

    html += H.field('Key Facilities',
      H.textInput('key_facilities',
        isPlot ? 'e.g. Gated Colony, Wide Road, Water Supply' : 'e.g. 24hr Security, CCTV, Visitor Parking'),
      'Separate each facility with a comma');

    return { id: 'basics', title: 'Basics', icon: '📝', html: html };
  }

  /* ── PANEL 2a: OWNER PLOT DETAILS ────────────────────────── */
  function ownerPlotDetailsPanel() {
    var html = plotSpecificFields();
    return { id: 'details', title: 'Plot Details', icon: '📋', html: html };
  }

  /* ── PANEL 2b: DEALER PLOT DETAILS ──────────────────────── */
  // Dealer plot: same as owner but without construction status,
  // property age, transaction type, flooring, facing, property ownership
  // (facing and ownership are inside plotSpecificFields which already
  //  has the right subset — we reuse the same function)
  function dealerPlotDetailsPanel() {
    // plotSpecificFields already excludes construction status, property age,
    // transaction type, flooring — matches the dealer requirements exactly
    var html = plotSpecificFields();
    return { id: 'details', title: 'Plot Details', icon: '📋', html: html };
  }

  /* ── PANEL 2c: PROPERTY DETAILS (rooms/floors) ───────────── */
  function propertyDetailsPanel(pt, isCommercial, hasFloors, isMultiFloor, isDealer) {
    var html = '';

    html += H.sectionHead('Size & Layout');

    if (!isCommercial) {
      html += H.twoCol(
        H.field('BHK / Rooms', H.bhkSelect(), ''),
        H.field('Bedrooms', H.numberInput('bedrooms', '0', 0), '')
      );
    } else {
      html += H.field('Cabins / Rooms', H.numberInput('bedrooms', '0', 0), 'Number of cabins or private rooms');
    }

    html += H.bathroomFields(isCommercial);
    html += H.twoCol(
      H.field('Built-up Area (sq ft)', H.numberInput('area_sqft', 'e.g. 1200'), '', true),
      H.field('Carpet Area (sq ft)', H.numberInput('carpet_area_sqft', 'e.g. 950'), '')
    );

    if (isMultiFloor) {
      html += H.twoCol(
        H.field('Number of Floors', H.numberInput('total_floors', 'e.g. 2'), ''),
        H.field('Plot Area (sq ft)', H.numberInput('plot_area_sqft', 'e.g. 500'), '')
      );
    }

    if (hasFloors) {
      html += H.sectionHead('Floor Details');
      html += H.twoCol(
        H.field('Floor Number', H.textInput('floor_number', 'e.g. 3 or Ground or Basement'), ''),
        H.field('Total Floors in Building', H.numberInput('total_floors', 'e.g. 12'), '')
      );
    }

    html += H.sectionHead('Property Info');
    html += H.twoCol(
      H.field('Construction Status', H.constructionStatusSelect(), ''),
      H.field('Property Age', H.propertyAgeSelect(), '')
    );
    html += H.twoCol(
      H.field('Transaction Type',
        H.selectInput('transaction_type', [
          ['','Select'],['new_property','New Property'],['resale','Resale'],
        ]), ''),
      H.field('Property Ownership',
        H.selectInput('property_ownership', [
          ['','Select'],['freehold','Freehold'],['leasehold','Leasehold'],
          ['cooperative','Co-op Society'],['power_of_attorney','Power of Attorney'],
        ]), '')
    );

    html += H.twoCol(
      H.field('Facing', H.facingSelect(), ''),
      H.field('Flooring', H.flooringSelect(), '')
    );

    html += H.twoCol(
      H.field('Width of Facing Road',
        H.selectInput('width_of_facing_road', D.ROAD_FACING_OPTIONS), ''),
      H.field('Water Source',
        H.selectInput('water_source', D.WATER_SOURCE_OPTIONS), '')
    );

    html += H.overlookingField();
    html += H.field('Vastu Compliant', H.toggleSwitch('vastu_compliant', 'Yes, this property is Vastu compliant'), '');

    return { id: 'details', title: 'Details', icon: '📋', html: html };
  }

  /* ── PANEL 3: FURNISHING & AMENITIES ─────────────────────── */
  function furnishingPanel(isPlot, isCommercial) {
    var html = '';
    var amenList = isCommercial ? D.COMMERCIAL_AMENITIES : D.AMENITIES;

    if (!isPlot && !isCommercial) {
      html += H.sectionHead('Furnishing Status');
      html += H.field('', H.chipGroup('furnishing_status', [
        { key:'furnished',      label:'Furnished',      emoji:'🛋️' },
        { key:'semi_furnished', label:'Semi Furnished', emoji:'🪑' },
        { key:'unfurnished',    label:'Unfurnished',    emoji:'📦' },
      ], false), '');

      html += '<div id="furnItemsSection">';
      html += H.sectionHead("What's Available in the Property");
      html += '<p class="pp-hint-text" style="margin-bottom:12px">Check all items that are available</p>';
      html += H.field('', H.chipGroup('furnishing_items', D.FURNISHING_ITEMS, true), '');
      html += '</div>';
    }

    if (isPlot) {
      html += H.sectionHead('Plot Amenities');
      html += H.field('', H.chipGroup('plot_amenities', [
        { key:'park',          label:'Park / Garden',     emoji:'🌳' },
        { key:'street_lights', label:'Street Lights',     emoji:'💡' },
        { key:'water_supply',  label:'Water Supply',      emoji:'💧' },
        { key:'sewage',        label:'Sewage / Drainage', emoji:'🚰' },
        { key:'gated',         label:'Gated Colony',      emoji:'🏘️' },
        { key:'cctv',          label:'CCTV',              emoji:'📷' },
        { key:'security',      label:'Security Guard',    emoji:'👮' },
        { key:'playground',    label:'Playground',        emoji:'🎠' },
      ], true), '');
    } else {
      html += H.sectionHead('Amenities');
      html += H.field('', H.chipGroup('amenities', amenList, true), '');
    }

    if (!isPlot && !isCommercial) {
      html += H.sectionHead('Tenant Preferences');
      html += H.field('Preferred Tenants',
        H.selectInput('preferred_tenants', [
          ['','Any'],['family','Family'],['single_man','Single Man'],
          ['single_woman','Single Woman'],['company_lease','Company Lease'],['any','Any'],
        ]), '');
      // NOTE: Min Price (₹) removed as requested
    }

    if (isCommercial) {
      html += H.sectionHead('Commercial Details');
      html += H.twoCol(
        H.field('Furnishing Status',
          H.selectInput('furnishing_status_com', [
            ['','Select'],['furnished','Furnished'],['semi_furnished','Semi-Furnished'],['bare_shell','Bare Shell'],
          ]), ''),
        H.field('Lock-in Period',
          H.textInput('lock_in_period', 'e.g. 11 months'), '')
      );
    }

    return { id: 'furnishing', title: 'Amenities', icon: '✨', html: html };
  }

  /* ── MAIN BUILDER ────────────────────────────────────────── */
  function getPanels(cat, pt) {
    var isPlot       = D.PLOT_TYPES.indexOf(pt)       > -1;
    var hasFloors    = D.FLOOR_TYPES.indexOf(pt)      > -1;
    var isMultiFloor = D.MULTI_FLOOR_TYPES.indexOf(pt) > -1;
    var isCommercial = (cat === 'commercial');

    // Detect dealer via PP_CORE state (set by pp-init.js)
    var isDealer = (typeof PP_CORE !== 'undefined' && PP_CORE.state.sellerType === 'dealer');

    var panels = [];
    panels.push(basicsPanel(isPlot, isCommercial));

    if (isPlot) {
      // Both owner and dealer use the same plot details panel
      // (plotSpecificFields already has the right subset for both)
      panels.push(ownerPlotDetailsPanel());
      panels.push(furnishingPanel(true, isCommercial));
    } else {
      panels.push(propertyDetailsPanel(pt, isCommercial, hasFloors, isMultiFloor, isDealer));
      panels.push(furnishingPanel(false, isCommercial));
    }

    panels.push(PP_MEDIA.mediaPanel());
    return panels;
  }

  return { getPanels: getPanels };
})();