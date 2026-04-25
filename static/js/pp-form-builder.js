/**
 * pp-form-builder.js
 * Panels for Builder seller type.
 * Depends on: pp-data.js, pp-helpers.js, pp-media.js
 */
'use strict';

var PP_BUILDER = (function () {
  var H = PP_H;
  var D = PP_DATA;

  /* ── PANEL 1: PROJECT INFO ───────────────────────────────── */
  function projectPanel(isPlot) {
    var html = H.listingTypeBlock(false);

    html += H.twoCol(
      H.field('Project Name', H.textInput('project_name', 'e.g. Sunrise Heights'), '', true),
      H.field('RERA ID', H.textInput('rera_id', 'RERA registration number'), '', false, true)
    );

    html += H.field('Property Title',
      H.textInput('title', isPlot
        ? 'e.g. Residential Plots in Sunrise Township'
        : 'e.g. 3BHK in Sunrise Heights'),
      '', true);

    html += H.twoCol(
      // NOTE: Min Price (₹) removed — only Price shown
      H.field('Price (₹)', H.prefixInput('price', isPlot ? 'e.g. 2500000' : 'e.g. 5000000', '₹'), isPlot ? 'Starting price per plot' : 'Unit price', true),
      H.field('Total Units in Project', H.numberInput('total_units', 'e.g. 120'), '')
    );

    if (isPlot) {
      html += H.twoCol(
        H.field('Min Plot Size', H.numberInput('min_area', 'Min sq ft'), ''),
        H.field('Max Plot Size', H.numberInput('max_area', 'Max sq ft'), '')
      );
    }

    html += H.field('Project Description',
      H.textarea('description', 'Describe the project, USPs, location advantages, infrastructure…', 4),
      '', true);
    html += H.field('Key Highlights',
      H.textarea('key_highlights', 'Why invest here? e.g. RERA approved, gated township, metro connectivity…', 3), '');
    html += H.field('Key Facilities',
      H.textInput('key_facilities', 'e.g. 24hr Security, Club House, Swimming Pool'),
      'Comma-separated');

    return { id: 'project', title: 'Project', icon: '🏗️', html: html };
  }

  /* ── PANEL 2: LOCATION ───────────────────────────────────── */
  function locationPanel() {
    var html = '';

    html += H.twoCol(
      H.field('City', H.textInput('city', 'e.g. Ludhiana'), '', true),
      H.field('State', H.textInput('state', 'e.g. Punjab'), '')
    );
    html += H.twoCol(
      H.field('Locality / Area', H.textInput('location', 'e.g. Model Town'), ''),
      H.field('Project Address', H.textInput('address', 'Site address / landmark'), '')
    );
    html += H.twoCol(
      H.field('Construction Status', H.constructionStatusSelect(), '', true),
      H.field('Expected Possession', H.textInput('possession_date', 'e.g. Dec 2026'), '')
    );
    html += H.twoCol(
      H.field('Width of Facing Road',
        H.selectInput('width_of_facing_road', D.ROAD_FACING_OPTIONS), ''),
      H.field('Approved By',
        H.selectInput('approved_by', [
          ['','Select'],['rera','RERA Approved'],['municipality','Municipality'],
          ['gram_panchayat','Gram Panchayat'],['other','Other'],
        ]), '')
    );

    return { id: 'location', title: 'Location', icon: '📍', html: html };
  }

  /* ── PANEL 3a: BUILDER PLOT UNIT DETAILS ─────────────────── */
  // Flooring REMOVED from plot panel as requested
  function plotUnitPanel() {
    var html = '';

    html += H.sectionHead('What Type of Plot?');
    html += H.field('Plot Type',
      H.chipGroup('plot_type', [
        { key: 'residential_plot',  label: 'Residential Plot',   emoji: '🏠' },
        { key: 'commercial_plot',   label: 'Commercial Plot',    emoji: '🏢' },
        { key: 'agricultural_land', label: 'Agricultural Land',  emoji: '🌾' },
        { key: 'industrial_land',   label: 'Industrial Land',    emoji: '🏭' },
      ], false),
      'Select the type of plot in this project', true);

    html += H.sectionHead('Plot Dimensions');
    html += H.threeCol(
      H.field('Min Plot Area', H.numberInput('min_area', 'Min'), ''),
      H.field('Max Plot Area', H.numberInput('max_area', 'Max'), ''),
      H.field('Area Unit', H.selectInput('area_unit', D.AREA_UNIT_OPTIONS), '')
    );

    html += H.twoCol(
      H.field('Plot Length', H.textInput('plot_length', 'e.g. 20 ft'), ''),
      H.field('Plot Width',  H.textInput('plot_width',  'e.g. 10 ft'), '')
    );

    html += H.twoCol(
      H.field('Facing', H.selectInput('facing', D.PLOT_FACING_OPTIONS), ''),
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
      'Select all utilities available');

    html += H.sectionHead('Legal & Approvals');
    html += H.field('',
      H.chipGroup('legal_status', [
        { key: 'clear_title',    label: 'Clear Title',    emoji: '📄' },
        { key: 'loan_approved',  label: 'Loan Approved',  emoji: '🏦' },
        { key: 'registry_ready', label: 'Registry Ready', emoji: '✅' },
      ], true),
      'Select all that apply');

    html += H.twoCol(
      H.field('Approved for Construction',
        H.selectInput('approved_for_construction', [
          ['','Select'],['yes','Yes'],['no','No'],
        ]), ''),
      H.field('Water Source', H.selectInput('water_source', D.WATER_SOURCE_OPTIONS), '')
    );

    html += H.twoCol(
      H.field('Boundary Wall',
        H.selectInput('boundary_wall', [
          ['','Select'],['yes','Yes'],['no','No'],['partial','Partial'],
        ]), ''),
      H.field('Property Ownership',
        H.selectInput('property_ownership', [
          ['','Select'],['freehold','Freehold'],['leasehold','Leasehold'],
        ]), '')
    );

    // NOTE: Flooring REMOVED from builder residential plot as requested
    html += H.field('Vastu Compliant', H.toggleSwitch('vastu_compliant', 'Yes, plots are Vastu compliant'), '');

    return { id: 'unit', title: 'Plot Details', icon: '📐', html: html };
  }

  /* ── PANEL 3b: BUILT UNIT DETAILS ────────────────────────── */
  function unitDetailsPanel(pt, isCommercial, hasFloors, isMultiFloor) {
    var html = '';

    html += H.sectionHead('Unit Configuration');
    if (!isCommercial) {
      html += H.twoCol(
        H.field('BHK Configuration', H.bhkSelect(), ''),
        H.field('Bedrooms', H.numberInput('bedrooms', '0', 0), '')
      );
    } else {
      html += H.field('Cabins / Rooms', H.numberInput('bedrooms', '0', 0), '');
    }
    html += H.bathroomFields(isCommercial);
    html += H.twoCol(
      H.field('Built-up Area (sq ft)', H.numberInput('area_sqft', 'e.g. 1500'), ''),
      H.field('Carpet Area (sq ft)', H.numberInput('carpet_area_sqft', 'e.g. 1100'), '')
    );

    if (isMultiFloor) {
      html += H.twoCol(
        H.field('Floors per Unit', H.numberInput('floors_per_unit', 'e.g. 2'), ''),
        H.field('Plot Area (sq ft)', H.numberInput('plot_area_sqft', 'e.g. 500'), '')
      );
    }

    if (hasFloors) {
      html += H.twoCol(
        H.field('Total Floors in Tower', H.numberInput('total_floors', 'e.g. 20'), ''),
        H.field('Facing', H.facingSelect(), '')
      );
    }

    html += H.sectionHead('Property Details');
    html += H.twoCol(
      H.field('Flooring', H.flooringSelect(), ''),
      H.field('Property Ownership',
        H.selectInput('property_ownership', [
          ['','Select'],['freehold','Freehold'],['leasehold','Leasehold'],['cooperative','Co-op Society'],
        ]), '')
    );
    html += H.field('Vastu Compliant', H.toggleSwitch('vastu_compliant', 'Yes, this project is Vastu compliant'), '');

    return { id: 'unit', title: 'Unit Details', icon: '📐', html: html };
  }

  /* ── PANEL 4: AMENITIES ──────────────────────────────────── */
  function amenitiesPanel(isPlot, isCommercial) {
    var html = '';
    var amenList = isCommercial ? D.COMMERCIAL_AMENITIES : D.AMENITIES;

    if (isPlot) {
      html += H.sectionHead('Township Amenities');
      html += H.field('', H.chipGroup('amenities', [
        { key:'park',          label:'Park / Garden',   emoji:'🌳' },
        { key:'street_lights', label:'Street Lights',   emoji:'💡' },
        { key:'water_supply',  label:'Water Supply',    emoji:'💧' },
        { key:'sewage',        label:'Sewage Network',  emoji:'🚰' },
        { key:'gated',         label:'Gated Entry',     emoji:'🏘️' },
        { key:'cctv',          label:'CCTV',            emoji:'📷' },
        { key:'security',      label:'Security Guard',  emoji:'👮' },
        { key:'club',          label:'Club House',      emoji:'🏛️' },
        { key:'playground',    label:'Playground',      emoji:'🎠' },
        { key:'shopping',      label:'Shopping Area',   emoji:'🛍️' },
      ], true), '');
    } else {
      html += H.sectionHead('Project Amenities');
      html += H.field('', H.chipGroup('amenities', amenList, true), '');

      if (!isCommercial) {
        html += H.sectionHead('Furnishing Status');
        html += H.field('', H.chipGroup('furnishing_status', [
          { key:'furnished',      label:'Furnished',      emoji:'🛋️' },
          { key:'semi_furnished', label:'Semi Furnished', emoji:'🪑' },
          { key:'unfurnished',    label:'Unfurnished',    emoji:'📦' },
        ], false), '');
      }
    }

    return { id: 'amenities', title: 'Amenities', icon: '✨', html: html };
  }

  /* ── MAIN BUILDER ────────────────────────────────────────── */
  function getPanels(cat, pt) {
    var isPlot       = D.PLOT_TYPES.indexOf(pt)        > -1;
    var hasFloors    = D.FLOOR_TYPES.indexOf(pt)       > -1;
    var isMultiFloor = D.MULTI_FLOOR_TYPES.indexOf(pt) > -1;
    var isCommercial = (cat === 'commercial');

    var panels = [];
    panels.push(projectPanel(isPlot));
    panels.push(locationPanel());

    if (isPlot) {
      panels.push(plotUnitPanel());
    } else {
      panels.push(unitDetailsPanel(pt, isCommercial, hasFloors, isMultiFloor));
    }

    panels.push(amenitiesPanel(isPlot, isCommercial));
    panels.push(PP_MEDIA.mediaPanel());
    return panels;
  }

  return { getPanels: getPanels };
})();