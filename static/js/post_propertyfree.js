/**
 * post_propertyfree.js
 * Dynamic seller-type → category → subtype → form engine
 *
 * Data from Django is read via json_script tags (no inline template tags
 * inside <script> blocks, so no JS linter errors):
 *   #django-form-errors  →  window.DJANGO_ERRORS
 *   #django-form-data    →  window.DJANGO_DATA
 */
(function () {
  'use strict';

  // ── READ DJANGO DATA FROM json_script TAGS ─────────────────────────────
  // Django renders:
  //   {{ form.errors|json_script:"django-form-errors" }}
  //   {{ form_data_json|json_script:"django-form-data" }}
  // as <script type="application/json" id="...">…</script> tags.
  // We parse them here — zero inline Django tags inside JS, zero linter errors.
  function readJsonScript(id) {
    var el = document.getElementById(id);
    if (!el) return {};
    try {
      var parsed = JSON.parse(el.textContent || el.innerText || '{}');
      // form_data_json arrives as a JSON-encoded string (json.dumps of a dict),
      // so it may need a second parse if Django's json_script double-encoded it.
      if (typeof parsed === 'string') {
        return JSON.parse(parsed);
      }
      return parsed;
    } catch (e) {
      return {};
    }
  }

  var DJANGO_ERRORS = readJsonScript('django-form-errors');
  var DJANGO_DATA   = readJsonScript('django-form-data');

  // ── STATE ──────────────────────────────────────────────────────────────
  var state = {
    sellerType:   '',
    category:     '',
    propertyType: '',
    step:         0,   // current form panel step (0-indexed)
    totalSteps:   0,
  };

  // ── SUBTYPE DEFINITIONS ────────────────────────────────────────────────
  var RESIDENTIAL_SUBTYPES = [
    { value: 'flat_apartment',          label: 'Flat / Apartment',          emoji: '🏢' },
    { value: 'independent_house_villa', label: 'Independent House / Villa',  emoji: '🏠' },
    { value: 'builder_floor',           label: 'Builder Floor',              emoji: '🏗️' },
    { value: 'plot_land_res',           label: 'Plot / Land',                emoji: '🌿' },
    { value: 'studio_1rk',             label: '1 RK / Studio Apartment',    emoji: '🚪' },
    { value: 'farmhouse',              label: 'Farmhouse',                  emoji: '🌾' },
  ];

  var COMMERCIAL_SUBTYPES = [
    { value: 'office',          label: 'Office Space',           emoji: '💼' },
    { value: 'retail',          label: 'Retail / Shop',          emoji: '🛍️' },
    { value: 'plot_land_com',   label: 'Commercial Plot',        emoji: '🌍' },
    { value: 'storage',         label: 'Warehouse / Storage',    emoji: '📦' },
    { value: 'dance_studio',    label: 'Dance / Fitness Studio', emoji: '🎭' },
    { value: 'coworking',       label: 'Co-working Space',       emoji: '💻' },
    { value: 'showroom',        label: 'Showroom',               emoji: '🚗' },
    { value: 'restaurant_cafe', label: 'Restaurant / Café',      emoji: '☕' },
  ];

  // Plot/land types (no BHK, no floors)
  var PLOT_TYPES  = ['plot_land_res', 'plot_land_com', 'farmhouse'];
  // Types where floor fields make sense
  var FLOOR_TYPES = ['flat_apartment', 'builder_floor', 'studio_1rk', 'office', 'retail', 'coworking', 'showroom'];

  // ── AMENITY & FURNISHING DATA ──────────────────────────────────────────
  var AMENITIES = [
    { key: 'lift',                 label: 'Lift',                 emoji: '🛗' },
    { key: 'park',                 label: 'Park',                 emoji: '🌳' },
    { key: 'gym',                  label: 'Gym',                  emoji: '💪' },
    { key: 'power_backup',         label: 'Power Backup',         emoji: '⚡' },
    { key: 'clubhouse',            label: 'Clubhouse',            emoji: '🏛️' },
    { key: 'parking',              label: 'Parking',              emoji: '🅿️' },
    { key: 'gas_pipeline',         label: 'Gas Pipeline',         emoji: '🔥' },
    { key: 'swimming_pool',        label: 'Swimming Pool',        emoji: '🏊' },
    { key: 'security_guards',      label: 'Security Guards',      emoji: '👮' },
    { key: 'cctv',                 label: 'CCTV',                 emoji: '📷' },
    { key: 'intercom',             label: 'Intercom',             emoji: '📞' },
    { key: 'rainwater_harvesting', label: 'Rainwater Harvesting', emoji: '💧' },
  ];

  var FURNISHING_ITEMS = [
    { key: 'water_purifier',  label: 'Water Purifier',  emoji: '💧' },
    { key: 'fan',             label: 'Fan',             emoji: '🌀' },
    { key: 'exhaust_fan',     label: 'Exhaust Fan',     emoji: '💨' },
    { key: 'dining_table',    label: 'Dining Table',    emoji: '🪑' },
    { key: 'geyser',          label: 'Geyser',          emoji: '🔥' },
    { key: 'light',           label: 'Light',           emoji: '💡' },
    { key: 'modular_kitchen', label: 'Modular Kitchen', emoji: '🍳' },
    { key: 'curtains',        label: 'Curtains',        emoji: '🪟' },
    { key: 'bed',             label: 'Bed',             emoji: '🛏️' },
    { key: 'wardrobe',        label: 'Wardrobe',        emoji: '🚪' },
    { key: 'sofa',            label: 'Sofa',            emoji: '🛋️' },
    { key: 'microwave',       label: 'Microwave',       emoji: '📡' },
    { key: 'ac',              label: 'AC',              emoji: '❄️' },
    { key: 'chimney',         label: 'Chimney',         emoji: '🏭' },
    { key: 'fridge',          label: 'Refrigerator',    emoji: '🧊' },
    { key: 'stove',           label: 'Stove',           emoji: '🔥' },
    { key: 'tv',              label: 'TV',              emoji: '📺' },
    { key: 'washing_machine', label: 'Washing Machine', emoji: '🌊' },
  ];

  var PG_AMENITIES = [
    { key: 'wifi',          label: 'Wi-Fi',          emoji: '📶' },
    { key: 'ac_room',       label: 'AC Room',        emoji: '❄️' },
    { key: 'attached_bath', label: 'Attached Bath',  emoji: '🚿' },
    { key: 'tv',            label: 'TV',             emoji: '📺' },
    { key: 'fridge',        label: 'Refrigerator',   emoji: '🧊' },
    { key: 'laundry',       label: 'Laundry',        emoji: '👕' },
    { key: 'meals',         label: 'Meals Included', emoji: '🍽️' },
    { key: 'housekeeping',  label: 'Housekeeping',   emoji: '🧹' },
    { key: 'cctv',          label: 'CCTV',           emoji: '📷' },
    { key: 'parking',       label: 'Parking',        emoji: '🅿️' },
  ];

  // ── PANEL DEFINITIONS ──────────────────────────────────────────────────
  function getPanels() {
    var s   = state.sellerType;
    var cat = state.category;
    var pt  = state.propertyType;
    var isPlot    = PLOT_TYPES.indexOf(pt) > -1;
    var hasFloors = FLOOR_TYPES.indexOf(pt) > -1;

    if (s === 'pg_owner') return pgPanels();
    if (s === 'builder')  return builderPanels(cat, pt, isPlot, hasFloors);
    return ownerDealerPanels(cat, pt, isPlot, hasFloors);
  }

  // ── HELPER: field row ──────────────────────────────────────────────────
  function field(label, input, hint, required) {
    var reqMark  = required ? '<span class="req-star">*</span>' : '';
    var hintHtml = hint ? '<p class="field-hint">' + hint + '</p>' : '';
    return '<div class="pp-field">' +
      '<label class="pp-label">' + label + reqMark + '</label>' +
      input + hintHtml +
      '</div>';
  }

  function textInput(name, placeholder, type) {
    type = type || 'text';
    return '<input type="' + type + '" name="' + name + '" placeholder="' + placeholder + '" class="pp-input">';
  }

  function numberInput(name, placeholder, min) {
    var minAttr = min !== undefined ? ' min="' + min + '"' : '';
    return '<input type="number" name="' + name + '" placeholder="' + placeholder + '" class="pp-input"' + minAttr + '>';
  }

  function selectInput(name, options) {
    var opts = options.map(function (o) {
      return '<option value="' + o[0] + '">' + o[1] + '</option>';
    }).join('');
    return '<select name="' + name + '" class="pp-input pp-select">' + opts + '</select>';
  }

  function textarea(name, placeholder, rows) {
    rows = rows || 4;
    return '<textarea name="' + name + '" placeholder="' + placeholder + '" class="pp-input pp-textarea" rows="' + rows + '"></textarea>';
  }

  function toggleSwitch(name, label) {
    return '<label class="pp-toggle">' +
      '<input type="checkbox" name="' + name + '" class="pp-toggle-input">' +
      '<span class="pp-toggle-track"><span class="pp-toggle-thumb"></span></span>' +
      '<span class="pp-toggle-label">' + label + '</span>' +
      '</label>';
  }

  function chipGroup(name, items, multi) {
    var inputType = multi ? 'checkbox' : 'radio';
    var chips = items.map(function (item) {
      return '<label class="pp-chip">' +
        '<input type="' + inputType + '" name="' + name + '" value="' + item.key + '" class="pp-chip-input">' +
        '<span class="pp-chip-emoji">' + item.emoji + '</span>' +
        '<span class="pp-chip-label">' + item.label + '</span>' +
        '</label>';
    }).join('');
    return '<div class="pp-chip-group">' + chips + '</div>';
  }

  function twoCol(left, right) {
    return '<div class="pp-two-col">' + left + right + '</div>';
  }

  function threeCol(a, b, c) {
    return '<div class="pp-three-col">' + a + b + c + '</div>';
  }

  function sectionHead(title) {
    return '<div class="pp-section-head">' + title + '</div>';
  }

  // ── LISTING TYPE TOGGLE ────────────────────────────────────────────────
  function listingTypeBlock(withPg) {
    var options = [
      { val: 'rent', icon: '🔑', label: 'For Rent',      sub: 'Monthly rent' },
      { val: 'sell', icon: '🏷️', label: 'For Sale',      sub: 'One-time sale' },
    ];
    if (withPg) {
      options.push({ val: 'pg', icon: '🛏️', label: 'PG / Co-living', sub: 'Per bed / room' });
    }

    var cards = options.map(function (o) {
      return '<label class="listing-type-card">' +
        '<input type="radio" name="listing_type_choice" value="' + o.val + '">' +
        '<span class="ltc-icon">' + o.icon + '</span>' +
        '<span class="ltc-label">' + o.label + '</span>' +
        '<span class="ltc-sub">' + o.sub + '</span>' +
        '</label>';
    }).join('');

    return '<div class="pp-field field-full">' +
      '<label class="pp-label">Listing Type<span class="req-star">*</span></label>' +
      '<div class="listing-type-group">' + cards + '</div>' +
      '</div>';
  }

  // ── MEDIA PANEL (common to all) ────────────────────────────────────────
  function mediaPanel() {
    return {
      id: 'media', title: 'Photos & Video', icon: '📸',
      html:
        '<div class="pp-panel-intro">Listings with photos get <strong>3× more inquiries</strong>.</div>' +

        '<div class="pp-field field-full">' +
          '<label class="pp-label">Property Photos<span class="req-star">*</span></label>' +
          '<div class="drop-zone" id="dropZone">' +
            '<input type="file" name="property_images" id="photoInput" multiple accept="image/*" class="drop-input">' +
            '<div class="drop-zone-content" id="dropZoneContent">' +
              '<div class="dz-icon">📷</div>' +
              '<p class="dz-title">Drag &amp; drop photos here</p>' +
              '<p class="dz-sub">or <span class="dz-link">click to browse</span></p>' +
              '<p class="dz-note">JPG · PNG · WEBP · Max 5 MB each · Up to 15 photos</p>' +
            '</div>' +
          '</div>' +
          '<div class="photo-preview-grid" id="photoPreviewGrid"></div>' +
        '</div>' +

        '<div class="pp-field field-full">' +
          '<label class="pp-label">Property Video <span class="opt-tag">optional</span></label>' +
          '<label class="file-btn-label" for="videoInput">' +
            '<span>🎬</span> <span id="videoFileName">Choose video…</span>' +
          '</label>' +
          '<input type="file" name="property_video" id="videoInput" accept="video/*" class="hidden-file-input">' +
          '<p class="field-hint">MP4 recommended · Max 50 MB</p>' +
        '</div>',
    };
  }

  // ══════════════════════════════════════════════════════════════════════
  //  OWNER / DEALER PANELS
  // ══════════════════════════════════════════════════════════════════════
  function ownerDealerPanels(cat, pt, isPlot, hasFloors) {
    var panels = [];

    // ── Panel 1: Basics ──────────────────────────────────────────────
    var basicsHtml = listingTypeBlock(false);

    basicsHtml += field('Property Title', textInput('title', 'e.g. Spacious 3BHK near Metro, Ludhiana'), '', true);
    basicsHtml += twoCol(
      field('Price (₹)', '<div class="input-pfx"><span>₹</span>' + numberInput('price', 'e.g. 15000') + '</div>', 'Rent/month or sale price', true),
      field('City', textInput('city', 'e.g. Ludhiana'), '', true)
    );
    basicsHtml += twoCol(
      field('State', textInput('state', 'e.g. Punjab'), ''),
      field('Locality / Area', textInput('location', 'e.g. Model Town'), '')
    );
    basicsHtml += field('Full Address', textInput('address', 'House No., Street, Society…'), '');
    basicsHtml += field('Description', textarea('description', 'Describe the property, nearby landmarks, transport access…', 4), '', true);
    basicsHtml += field('Key Highlights', textarea('key_highlights', 'Why should someone consider this property? e.g. Corner unit, park-facing, recently renovated…', 3), 'Selling points that make your property stand out');
    basicsHtml += field('Key Facilities', textInput('key_facilities', 'e.g. 24hr Security, CCTV, Visitor Parking'), 'Separate each facility with a comma');

    panels.push({ id: 'basics', title: 'Basics', icon: '📝', html: basicsHtml });

    // ── Panel 2: Property Details ────────────────────────────────────
    var detailsHtml = '';

    if (!isPlot) {
      detailsHtml += sectionHead('Size & Layout');
      detailsHtml += twoCol(
        field('BHK / Rooms',
          selectInput('bhk', [
            ['', 'Select'], ['1rk', '1 RK'], ['1bhk', '1 BHK'], ['2bhk', '2 BHK'],
            ['3bhk', '3 BHK'], ['4bhk', '4 BHK'], ['5bhk+', '5 BHK+'],
          ]), ''),
        field('Bedrooms', numberInput('bedrooms', '0', 0), '')
      );
      detailsHtml += twoCol(
        field('Bathrooms', numberInput('bathrooms', '0', 0), ''),
        field('Area (sq ft)', numberInput('area_sqft', 'e.g. 1200'), '')
      );
    } else {
      detailsHtml += sectionHead('Plot Size');
      detailsHtml += threeCol(
        field('Min Area', numberInput('min_area', 'Min'), ''),
        field('Max Area', numberInput('max_area', 'Max'), ''),
        field('Unit', selectInput('area_unit', [
          ['sqft', 'Sq Ft'], ['sqyard', 'Sq Yards'], ['sqmeter', 'Sq Meter'],
          ['acres', 'Acres'], ['marlas', 'Marlas'], ['cents', 'Cents'],
        ]), '')
      );
      detailsHtml += twoCol(
        field('Width of Facing Road', textInput('width_of_facing_road', 'e.g. 30 ft'), ''),
        field('Water Source', selectInput('water_source', [
          ['', 'Select'], ['borewell', 'Borewell'], ['municipal', 'Municipal'], ['both', 'Both'],
        ]), '')
      );
    }

    if (hasFloors) {
      detailsHtml += sectionHead('Floor Details');
      detailsHtml += twoCol(
        field('Floor Number', textInput('floor_number', 'e.g. 3 or Ground'), ''),
        field('Total Floors in Building', numberInput('total_floors', 'e.g. 12'), '')
      );
    }

    detailsHtml += sectionHead('Property Info');
    detailsHtml += twoCol(
      field('Construction Status', selectInput('construction_status', [
        ['', 'Select'], ['new_launch', 'New Launch'],
        ['under_construction', 'Under Construction'], ['ready_to_move', 'Ready To Move'],
      ]), ''),
      field('Property Age', selectInput('property_age', [
        ['', 'Select'], ['0-1', '0-1 Years'], ['1-5', '1-5 Years'],
        ['5-10', '5-10 Years'], ['10-20', '10-20 Years'], ['20+', '20+ Years'],
      ]), '')
    );
    detailsHtml += twoCol(
      field('Transaction Type', selectInput('transaction_type', [
        ['', 'Select'], ['new_property', 'New Property'], ['resale', 'Resale'],
      ]), ''),
      field('Property Ownership', selectInput('property_ownership', [
        ['', 'Select'], ['freehold', 'Freehold'], ['leasehold', 'Leasehold'],
        ['cooperative', 'Co-op Society'], ['power_of_attorney', 'Power of Attorney'],
      ]), '')
    );
    detailsHtml += twoCol(
      field('Facing', selectInput('facing', [
        ['', 'Select'], ['east', 'East'], ['west', 'West'], ['north', 'North'], ['south', 'South'],
        ['north_east', 'North-East'], ['north_west', 'North-West'],
        ['south_east', 'South-East'], ['south_west', 'South-West'],
      ]), ''),
      field('Flooring', selectInput('flooring', [
        ['', 'Select'], ['marble', 'Marble'], ['vitrified_tiles', 'Vitrified Tiles'],
        ['ceramic_tiles', 'Ceramic Tiles'], ['wooden', 'Wooden'],
        ['granite', 'Granite'], ['mosaic', 'Mosaic'], ['normal_tiles', 'Normal Tiles'],
      ]), '')
    );
    if (!isPlot) {
      detailsHtml += twoCol(
        field('Width of Facing Road', textInput('width_of_facing_road', 'e.g. 30 ft'), ''),
        field('Water Source', selectInput('water_source', [
          ['', 'Select'], ['borewell', 'Borewell'], ['municipal', 'Municipal'], ['both', 'Both'],
        ]), '')
      );
    }
    detailsHtml += field('Overlooking', chipGroup('overlooking', [
      { key: 'garden',      label: 'Garden / Park', emoji: '🌳' },
      { key: 'main_road',   label: 'Main Road',     emoji: '🛣️' },
      { key: 'pool',        label: 'Pool',          emoji: '🏊' },
      { key: 'club',        label: 'Clubhouse',     emoji: '🏛️' },
      { key: 'other_units', label: 'Other Units',   emoji: '🏢' },
    ], true), 'Select all that apply');
    detailsHtml += field('Vastu Compliant', toggleSwitch('vastu_compliant', 'Yes, this property is Vastu compliant'), '');

    panels.push({ id: 'details', title: 'Details', icon: '📋', html: detailsHtml });

    // ── Panel 3: Furnishing & Amenities ──────────────────────────────
    var furnHtml = '';
    if (!isPlot && cat !== 'commercial') {
      furnHtml += sectionHead('Furnishing Status');
      furnHtml += field('', chipGroup('furnishing_status', [
        { key: 'furnished',      label: 'Furnished',      emoji: '🛋️' },
        { key: 'semi_furnished', label: 'Semi Furnished', emoji: '🪑' },
        { key: 'unfurnished',    label: 'Unfurnished',    emoji: '📦' },
      ], false), '');

      furnHtml += '<div id="furnItemsSection">';
      furnHtml += sectionHead('Furnishing Items Available');
      furnHtml += '<p class="pp-hint-text">Check all items that are available in the property</p>';
      furnHtml += field('', chipGroup('furnishing_items', FURNISHING_ITEMS, true), '');
      furnHtml += '</div>';
    }

    furnHtml += sectionHead('Amenities');
    furnHtml += field('', chipGroup('amenities', AMENITIES, true), '');

    if (cat === 'residential' || cat === '') {
      furnHtml += sectionHead('Tenant Preferences');
      furnHtml += twoCol(
        field('Preferred Tenants', selectInput('preferred_tenants', [
          ['', 'Any'], ['family', 'Family'], ['single_man', 'Single Man'],
          ['single_woman', 'Single Woman'], ['company_lease', 'Company Lease'],
          ['any', 'Any'],
        ]), ''),
        field('Min Price (₹)', '<div class="input-pfx"><span>₹</span>' + numberInput('min_price', 'Min') + '</div>', '')
      );
    }

    panels.push({ id: 'furnishing', title: 'Amenities', icon: '✨', html: furnHtml });

    // ── Panel 4: Media ───────────────────────────────────────────────
    panels.push(mediaPanel());

    return panels;
  }

  // ══════════════════════════════════════════════════════════════════════
  //  BUILDER PANELS
  // ══════════════════════════════════════════════════════════════════════
  function builderPanels(cat, pt, isPlot, hasFloors) {
    var panels = [];

    // Panel 1: Project Info
    var projHtml = listingTypeBlock(false);
    projHtml += twoCol(
      field('Project Name', textInput('project_name', 'e.g. Sunrise Heights'), '', true),
      field('RERA ID', textInput('rera_id', 'RERA registration number'), '')
    );
    projHtml += field('Property Title', textInput('title', 'e.g. 3BHK in Sunrise Heights'), '', true);
    projHtml += twoCol(
      field('Price (₹)', '<div class="input-pfx"><span>₹</span>' + numberInput('price', 'e.g. 5000000') + '</div>', '', true),
      field('Total Units in Project', numberInput('total_units', 'e.g. 120'), '')
    );
    projHtml += field('Description', textarea('description', 'Describe the project, USPs, location advantages…', 4), '', true);
    projHtml += field('Key Highlights', textarea('key_highlights', 'Why invest here? E.g. RERA approved, near airport, smart home tech…', 3), '');
    projHtml += field('Key Facilities', textInput('key_facilities', 'e.g. 24hr Security, CCTV, Club House'), 'Comma-separated');
    panels.push({ id: 'project', title: 'Project', icon: '🏗️', html: projHtml });

    // Panel 2: Location
    var locHtml = '';
    locHtml += twoCol(
      field('City', textInput('city', 'e.g. Ludhiana'), '', true),
      field('State', textInput('state', 'e.g. Punjab'), '')
    );
    locHtml += twoCol(
      field('Locality / Area', textInput('location', 'e.g. Model Town'), ''),
      field('Address', textInput('address', 'Project address / site'), '')
    );
    locHtml += twoCol(
      field('Construction Status', selectInput('construction_status', [
        ['', 'Select'], ['new_launch', 'New Launch'],
        ['under_construction', 'Under Construction'], ['ready_to_move', 'Ready To Move'],
      ]), '', true),
      field('Expected Possession', textInput('possession_date', 'e.g. Dec 2026'), '')
    );
    panels.push({ id: 'location', title: 'Location', icon: '📍', html: locHtml });

    // Panel 3: Unit Details
    var unitHtml = '';
    if (!isPlot) {
      unitHtml += twoCol(
        field('BHK Configuration', selectInput('bhk', [
          ['', 'Select'], ['1rk', '1 RK'], ['1bhk', '1 BHK'], ['2bhk', '2 BHK'],
          ['3bhk', '3 BHK'], ['4bhk', '4 BHK'], ['5bhk+', '5 BHK+'],
        ]), ''),
        field('Bedrooms', numberInput('bedrooms', '0', 0), '')
      );
      unitHtml += twoCol(
        field('Bathrooms', numberInput('bathrooms', '0', 0), ''),
        field('Area (sq ft)', numberInput('area_sqft', 'e.g. 1500'), '')
      );
      if (hasFloors) {
        unitHtml += twoCol(
          field('Total Floors', numberInput('total_floors', 'e.g. 20'), ''),
          field('Facing', selectInput('facing', [
            ['', 'Select'], ['east', 'East'], ['west', 'West'], ['north', 'North'], ['south', 'South'],
            ['north_east', 'North-East'], ['north_west', 'North-West'],
            ['south_east', 'South-East'], ['south_west', 'South-West'],
          ]), '')
        );
      }
    } else {
      unitHtml += threeCol(
        field('Min Area', numberInput('min_area', 'Min'), ''),
        field('Max Area', numberInput('max_area', 'Max'), ''),
        field('Unit', selectInput('area_unit', [
          ['sqft', 'Sq Ft'], ['sqyard', 'Sq Yards'], ['sqmeter', 'Sq Meter'],
          ['acres', 'Acres'], ['marlas', 'Marlas'],
        ]), '')
      );
    }
    unitHtml += twoCol(
      field('Flooring', selectInput('flooring', [
        ['', 'Select'], ['marble', 'Marble'], ['vitrified_tiles', 'Vitrified Tiles'],
        ['ceramic_tiles', 'Ceramic Tiles'], ['wooden', 'Wooden'], ['granite', 'Granite'],
      ]), ''),
      field('Property Ownership', selectInput('property_ownership', [
        ['', 'Select'], ['freehold', 'Freehold'], ['leasehold', 'Leasehold'], ['cooperative', 'Co-op Society'],
      ]), '')
    );
    unitHtml += field('Vastu Compliant', toggleSwitch('vastu_compliant', 'Yes, this project is Vastu compliant'), '');
    panels.push({ id: 'unit', title: 'Unit Details', icon: '📐', html: unitHtml });

    // Panel 4: Amenities
    var amentHtml = sectionHead('Project Amenities');
    amentHtml += field('', chipGroup('amenities', AMENITIES, true), '');
    amentHtml += sectionHead('Furnishing');
    amentHtml += field('', chipGroup('furnishing_status', [
      { key: 'furnished',      label: 'Furnished',      emoji: '🛋️' },
      { key: 'semi_furnished', label: 'Semi Furnished', emoji: '🪑' },
      { key: 'unfurnished',    label: 'Unfurnished',    emoji: '📦' },
    ], false), '');
    panels.push({ id: 'amenities', title: 'Amenities', icon: '✨', html: amentHtml });

    // Panel 5: Media
    panels.push(mediaPanel());

    return panels;
  }

  // ══════════════════════════════════════════════════════════════════════
  //  PG PANELS
  // ══════════════════════════════════════════════════════════════════════
  function pgPanels() {
    var panels = [];

    // Panel 1: PG Basics
    var basicsHtml = '';
    basicsHtml += field('PG Name / Title', textInput('title', 'e.g. Sai PG for Girls, Model Town'), '', true);
    basicsHtml += twoCol(
      field('Monthly Rent (₹)', '<div class="input-pfx"><span>₹</span>' + numberInput('price', 'e.g. 8000') + '</div>', 'Per person / per bed', true),
      field('PG For', chipGroup('pg_for', [
        { key: 'male',   label: 'Male',   emoji: '👨' },
        { key: 'female', label: 'Female', emoji: '👩' },
        { key: 'any',    label: 'Any',    emoji: '👥' },
      ], false))
    );
    basicsHtml += twoCol(
      field('City', textInput('city', 'e.g. Ludhiana'), '', true),
      field('State', textInput('state', 'e.g. Punjab'), '')
    );
    basicsHtml += twoCol(
      field('Locality', textInput('location', 'e.g. Model Town'), ''),
      field('Full Address', textInput('address', 'House No., Street…'), '')
    );
    basicsHtml += field('Description', textarea('description', 'Describe your PG — rooms, rules, nearby colleges, transport…', 4), '', true);
    basicsHtml += field('Key Facilities', textInput('key_facilities', 'e.g. 24hr Security, CCTV, Common Kitchen'), 'Comma-separated');
    panels.push({ id: 'basics', title: 'Basics', icon: '📝', html: basicsHtml });

    // Panel 2: PG Details
    var detailsHtml = '';
    detailsHtml += twoCol(
      field('Total Beds / Rooms', numberInput('bedrooms', '0', 0), ''),
      field('Bathrooms', numberInput('bathrooms', '0', 0), '')
    );
    detailsHtml += twoCol(
      field('Notice Period', textInput('pg_notice_period', 'e.g. 30 days'), ''),
      field('Preferred Tenants', selectInput('preferred_tenants', [
        ['', 'Any'], ['family', 'Family'], ['single_man', 'Single Man'],
        ['single_woman', 'Single Woman'], ['any', 'Any'],
      ]), '')
    );
    detailsHtml += sectionHead('PG Amenities & Facilities');
    detailsHtml += field('', chipGroup('pg_common_areas', PG_AMENITIES, true), 'Select all that apply');
    detailsHtml += field('Vastu Compliant', toggleSwitch('vastu_compliant', 'Yes, Vastu compliant'), '');
    panels.push({ id: 'details', title: 'Details', icon: '🏠', html: detailsHtml });

    // Panel 3: Media
    panels.push(mediaPanel());

    return panels;
  }

  // ── DOM HELPERS ────────────────────────────────────────────────────────
  function $(id) { return document.getElementById(id); }
  function show(id) { var el = $(id); if (el) el.classList.remove('hidden'); }
  function hide(id) { var el = $(id); if (el) el.classList.add('hidden'); }

  // ── SCREENS ────────────────────────────────────────────────────────────
  var screens = ['screen-seller', 'screen-category', 'screen-subtype', 'formWrap'];
  function showScreen(id) {
    screens.forEach(function (s) {
      var el = $(s);
      if (el) {
        if (s === id) el.classList.remove('hidden');
        else          el.classList.add('hidden');
      }
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // ── SELLER SELECTION ──────────────────────────────────────────────────
  document.querySelectorAll('.seller-card').forEach(function (card) {
    card.addEventListener('click', function () {
      state.sellerType = this.dataset.seller;
      $('hSellerType').value = state.sellerType;

      if (state.sellerType === 'pg_owner') {
        state.category     = 'pg';
        state.propertyType = 'pg_hostel';
        $('hCategory').value     = 'pg';
        $('hPropertyType').value = 'pg_hostel';
        $('hListingType').value  = 'pg';
        buildAndShowForm();
      } else {
        var eyebrow = { owner: 'Owner', builder: 'Builder', dealer: 'Dealer / Agent' };
        $('catEyebrow').textContent = eyebrow[state.sellerType] || '';
        showScreen('screen-category');
      }
    });
  });

  // ── CATEGORY SELECTION ────────────────────────────────────────────────
  document.querySelectorAll('.cat-card').forEach(function (card) {
    card.addEventListener('click', function () {
      state.category = this.dataset.cat;
      $('hCategory').value = state.category;

      var subtypes = state.category === 'commercial' ? COMMERCIAL_SUBTYPES : RESIDENTIAL_SUBTYPES;
      var eyebrow  = state.category === 'commercial' ? 'Commercial' : 'Residential';
      $('subtypeEyebrow').textContent = eyebrow;

      var grid = $('subtypeGrid');
      grid.innerHTML = '';
      subtypes.forEach(function (st) {
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'subtype-card';
        btn.dataset.value = st.value;
        btn.innerHTML =
          '<span class="stc-emoji">' + st.emoji + '</span>' +
          '<span class="stc-label">' + st.label + '</span>';
        btn.addEventListener('click', function () {
          state.propertyType = this.dataset.value;
          $('hPropertyType').value = state.propertyType;
          buildAndShowForm();
        });
        grid.appendChild(btn);
      });
      showScreen('screen-subtype');
    });
  });

  // ── BACK BUTTONS ──────────────────────────────────────────────────────
  $('backToSeller').addEventListener('click', function () { showScreen('screen-seller'); });
  $('backToCategory').addEventListener('click', function () { showScreen('screen-category'); });

  // ── BUILD FORM ────────────────────────────────────────────────────────
  function buildAndShowForm() {
    var panels = getPanels();
    state.totalSteps = panels.length;
    state.step = 0;

    // Build step nav
    var nav = $('ppStepsNav');
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
        '<span class="pp-step-num">'  + (i + 1)     + '</span>' +
        '<span class="pp-step-icon">' + panel.icon  + '</span>' +
        '<span class="pp-step-lbl">'  + panel.title + '</span>';
      pill.addEventListener('click', function () {
        var t = parseInt(this.dataset.step, 10);
        if (t < state.step) goToStep(t);
      });
      nav.appendChild(pill);
    });

    // Build breadcrumb
    var sellerLabels = { pg_owner: 'PG Owner', owner: 'Owner', builder: 'Builder', dealer: 'Dealer' };
    var catLabels    = { residential: 'Residential', commercial: 'Commercial', pg: 'PG' };
    var subtypeLabel = '';
    var allSubs = RESIDENTIAL_SUBTYPES.concat(COMMERCIAL_SUBTYPES);
    for (var i = 0; i < allSubs.length; i++) {
      if (allSubs[i].value === state.propertyType) { subtypeLabel = allSubs[i].label; break; }
    }
    $('ppBreadcrumb').innerHTML =
      '<span class="bc-item">' + (sellerLabels[state.sellerType] || '') + '</span>' +
      (state.category && state.category !== 'pg'
        ? '<span class="bc-sep">›</span><span class="bc-item">' + (catLabels[state.category] || '') + '</span>'
        : '') +
      (subtypeLabel
        ? '<span class="bc-sep">›</span><span class="bc-item bc-active">' + subtypeLabel + '</span>'
        : '') +
      '<button type="button" class="bc-change" id="bcChange">Change</button>';

    var bcChange = $('bcChange');
    if (bcChange) {
      bcChange.addEventListener('click', function () {
        if (state.sellerType === 'pg_owner') showScreen('screen-seller');
        else showScreen('screen-subtype');
      });
    }

    // Render all panels into form body
    var body = $('ppFormBody');
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

    initImageUpload();
    initFurnishingToggle();
    initListingTypeSync();

    showScreen('formWrap');
    updateNavAndProgress();
  }

  // ── STEP NAVIGATION ───────────────────────────────────────────────────
  function goToStep(n) {
    var oldPanel = $('pp-panel-' + state.step);
    var newPanel = $('pp-panel-' + n);
    if (oldPanel) oldPanel.classList.remove('active');
    if (newPanel) newPanel.classList.add('active');
    state.step = n;
    updateNavAndProgress();
    $('ppFormBody').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function updateNavAndProgress() {
    var pct = state.totalSteps > 1 ? (state.step / (state.totalSteps - 1)) * 100 : 100;
    $('ppProgressFill').style.width = pct + '%';

    document.querySelectorAll('.pp-step-pill').forEach(function (pill) {
      var s = parseInt(pill.dataset.step, 10);
      pill.classList.toggle('active',    s === state.step);
      pill.classList.toggle('completed', s < state.step);
    });

    var isLast = state.step === state.totalSteps - 1;
    $('ppBtnBack').style.display = state.step === 0 ? 'none' : '';
    $('ppBtnNext').classList.toggle('hidden', isLast);
    $('ppBtnSubmit').classList.toggle('hidden', !isLast);
  }

  $('ppBtnNext').addEventListener('click', function () {
    if (validateCurrentPanel()) goToStep(state.step + 1);
  });

  $('ppBtnBack').addEventListener('click', function () {
    if (state.step > 0) {
      goToStep(state.step - 1);
    } else {
      if (state.sellerType === 'pg_owner') showScreen('screen-seller');
      else showScreen('screen-subtype');
    }
  });

  // ── VALIDATE PANEL ────────────────────────────────────────────────────
  function validateCurrentPanel() {
    var panel = $('pp-panel-' + state.step);
    if (!panel) return true;
    var ok = true;

    panel.querySelectorAll('.pp-input[name]').forEach(function (el) {
      var fieldBlock = el.closest('.pp-field');
      var label      = fieldBlock && fieldBlock.querySelector('.pp-label');
      var isRequired = label && label.querySelector('.req-star');
      if (!isRequired) return;

      var val = el.value ? el.value.trim() : '';
      if (!val) {
        ok = false;
        el.classList.add('input-error');
        el.addEventListener('input', function () { el.classList.remove('input-error'); }, { once: true });
      }
    });

    panel.querySelectorAll('.listing-type-group').forEach(function (grp) {
      if (!grp.querySelector('input:checked')) {
        ok = false;
        grp.classList.add('group-error');
        grp.addEventListener('change', function () { grp.classList.remove('group-error'); }, { once: true });
      }
    });

    // Focus first error field
    if (!ok) {
      var firstError = panel.querySelector('.pp-input.input-error');
      if (firstError) firstError.focus();
    }

    return ok;
  }

  // ── LISTING TYPE SYNC ─────────────────────────────────────────────────
  function initListingTypeSync() {
    document.querySelectorAll('[name="listing_type_choice"]').forEach(function (radio) {
      radio.addEventListener('change', function () {
        $('hListingType').value = this.value;
      });
    });
    var checked = document.querySelector('[name="listing_type_choice"]:checked');
    if (!checked) {
      var first = document.querySelector('[name="listing_type_choice"]');
      if (first) { first.checked = true; $('hListingType').value = first.value; }
    }
  }

  // ── FURNISHING TOGGLE ─────────────────────────────────────────────────
  function initFurnishingToggle() {
    document.querySelectorAll('[name="furnishing_status"]').forEach(function (radio) {
      radio.addEventListener('change', function () {
        var sec = $('furnItemsSection');
        if (sec) sec.style.display = this.value === 'unfurnished' ? 'none' : '';
      });
    });
  }

  // ── IMAGE UPLOAD ──────────────────────────────────────────────────────
  function initImageUpload() {
    var dropZone    = $('dropZone');
    var photoInput  = $('photoInput');
    var previewGrid = $('photoPreviewGrid');
    var videoInput  = $('videoInput');
    var videoName   = $('videoFileName');
    if (!dropZone || !photoInput) return;

    var files = [];

    function renderPreviews() {
      previewGrid.innerHTML = '';
      files.forEach(function (file, i) {
        var reader = new FileReader();
        reader.onload = function (e) {
          var div = document.createElement('div');
          div.className = 'photo-thumb';
          div.innerHTML =
            '<img src="' + e.target.result + '" alt="Photo ' + (i + 1) + '">' +
            '<button type="button" class="photo-thumb-remove" data-index="' + i + '">✕</button>' +
            '<span class="photo-thumb-num">' + (i + 1) + '</span>';
          previewGrid.appendChild(div);
          div.querySelector('.photo-thumb-remove').addEventListener('click', function () {
            files.splice(parseInt(this.dataset.index, 10), 1);
            syncFileInput();
            renderPreviews();
          });
        };
        reader.readAsDataURL(file);
      });
      $('dropZoneContent').style.display = files.length > 0 ? 'none' : '';
    }

    function syncFileInput() {
      var dt = new DataTransfer();
      files.forEach(function (f) { dt.items.add(f); });
      photoInput.files = dt.files;
    }

    function addFiles(newFiles) {
      for (var i = 0; i < newFiles.length; i++) {
        if (files.length >= 15) break;
        if (newFiles[i].size > 5 * 1024 * 1024) { alert(newFiles[i].name + ' exceeds 5 MB'); continue; }
        files.push(newFiles[i]);
      }
      syncFileInput();
      renderPreviews();
    }

    dropZone.addEventListener('click', function () { photoInput.click(); });
    photoInput.addEventListener('change', function () { addFiles(this.files); });

    dropZone.addEventListener('dragover', function (e) { e.preventDefault(); dropZone.classList.add('drag-over'); });
    dropZone.addEventListener('dragleave', function () { dropZone.classList.remove('drag-over'); });
    dropZone.addEventListener('drop', function (e) {
      e.preventDefault();
      dropZone.classList.remove('drag-over');
      addFiles(e.dataTransfer.files);
    });

    if (videoInput && videoName) {
      videoInput.addEventListener('change', function () {
        videoName.textContent = this.files[0] ? this.files[0].name : 'Choose video…';
      });
    }
  }

  // ── RESTORE STATE AFTER DJANGO VALIDATION ERROR (POST → re-render) ────
  // Reads seller_type / property_type from the hidden inputs Django re-populates
  // on a failed POST, then rebuilds the form and restores all field values from
  // DJANGO_DATA (populated via json_script in the template).
  (function restoreOnError() {
    var sellerType   = $('hSellerType')   && $('hSellerType').value;
    var category     = $('hCategory')     && $('hCategory').value;
    var propertyType = $('hPropertyType') && $('hPropertyType').value;

    if (!sellerType || !propertyType) return;   // fresh GET — nothing to restore

    state.sellerType   = sellerType;
    state.category     = category;
    state.propertyType = propertyType;

    buildAndShowForm();

    // Restore plain text / select / textarea / number values
    Object.keys(DJANGO_DATA).forEach(function (name) {
      var val = DJANGO_DATA[name];
      if (!val) return;
      var el = document.querySelector('[name="' + name + '"]');
      if (el && el.type !== 'file') {
        el.value = val;
      }
    });

    // Highlight any server-side errors so the user can see them
    Object.keys(DJANGO_ERRORS).forEach(function (name) {
      var el = document.querySelector('[name="' + name + '"]');
      if (el) el.classList.add('input-error');
    });
  })();

  // ── INIT ──────────────────────────────────────────────────────────────
  $('ppBtnBack').style.display = 'none';

})();