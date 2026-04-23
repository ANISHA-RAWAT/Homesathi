/**
 * pp-data.js
 * All static data: subtypes, amenities, furnishing items, etc.
 */
'use strict';

var PP_DATA = (function () {

  var RESIDENTIAL_SUBTYPES = [
    { value: 'flat_apartment',           label: 'Flat / Apartment',          emoji: '🏢' },
    { value: 'independent_house_villa',  label: 'Independent House / Villa', emoji: '🏠' },
    { value: 'builder_floor',            label: 'Builder Floor',             emoji: '🏗️' },
    { value: 'plot_land_res',            label: 'Plot / Land',               emoji: '🌿' },
    { value: 'studio_1rk',              label: '1 RK / Studio Apartment',   emoji: '🚪' },
    { value: 'farmhouse',               label: 'Farmhouse',                 emoji: '🌾' },
  ];

  var COMMERCIAL_SUBTYPES = [
    { value: 'office',           label: 'Office Space',           emoji: '💼' },
    { value: 'retail',           label: 'Retail / Shop',          emoji: '🛍️' },
    { value: 'plot_land_com',    label: 'Commercial Plot',        emoji: '🌍' },
    { value: 'storage',          label: 'Warehouse / Storage',    emoji: '📦' },
    { value: 'dance_studio',     label: 'Dance / Fitness Studio', emoji: '🎭' },
    { value: 'coworking',        label: 'Co-working Space',       emoji: '💻' },
    { value: 'showroom',         label: 'Showroom',               emoji: '🚗' },
    { value: 'restaurant_cafe',  label: 'Restaurant / Café',      emoji: '☕' },
  ];

  // Plot types: NO rooms/floors/BHK — only land dimensions
  var PLOT_TYPES  = ['plot_land_res', 'plot_land_com'];

  // Types that sit on a specific floor inside a building
  var FLOOR_TYPES = ['flat_apartment', 'builder_floor', 'studio_1rk', 'office', 'retail', 'coworking', 'showroom'];

  // Types that have multiple floors themselves (not in a multi-storey building)
  var MULTI_FLOOR_TYPES = ['independent_house_villa', 'farmhouse', 'storage', 'dance_studio', 'restaurant_cafe'];

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

  var COMMERCIAL_AMENITIES = [
    { key: 'power_backup',    label: 'Power Backup',    emoji: '⚡' },
    { key: 'lift',            label: 'Lift',            emoji: '🛗' },
    { key: 'parking',         label: 'Parking',         emoji: '🅿️' },
    { key: 'cctv',            label: 'CCTV',            emoji: '📷' },
    { key: 'security_guards', label: 'Security Guards', emoji: '👮' },
    { key: 'fire_safety',     label: 'Fire Safety',     emoji: '🔥' },
    { key: 'wifi',            label: 'Wi-Fi',           emoji: '📶' },
    { key: 'cafeteria',       label: 'Cafeteria',       emoji: '☕' },
    { key: 'reception',       label: 'Reception Area',  emoji: '🏢' },
    { key: 'conference_room', label: 'Conference Room', emoji: '📋' },
    { key: 'ac',              label: 'Central AC',      emoji: '❄️' },
    { key: 'washroom',        label: 'Washroom',        emoji: '🚿' },
  ];

  var FURNISHING_ITEMS = [
    { key: 'bed',             label: 'Bed',             emoji: '🛏️' },
    { key: 'wardrobe',        label: 'Wardrobe',        emoji: '🪞' },
    { key: 'sofa',            label: 'Sofa',            emoji: '🛋️' },
    { key: 'dining_table',    label: 'Dining Table',    emoji: '🍽️' },
    { key: 'modular_kitchen', label: 'Modular Kitchen', emoji: '🍳' },
    { key: 'ac',              label: 'AC',              emoji: '❄️' },
    { key: 'fan',             label: 'Fan',             emoji: '🌀' },
    { key: 'geyser',          label: 'Geyser',          emoji: '🔥' },
    { key: 'water_purifier',  label: 'Water Purifier',  emoji: '💧' },
    { key: 'fridge',          label: 'Refrigerator',    emoji: '🧊' },
    { key: 'washing_machine', label: 'Washing Machine', emoji: '🫧' },
    { key: 'tv',              label: 'TV',              emoji: '📺' },
    { key: 'microwave',       label: 'Microwave',       emoji: '📡' },
    { key: 'chimney',         label: 'Chimney',         emoji: '🏭' },
    { key: 'stove',           label: 'Stove / Hob',     emoji: '🍲' },
    { key: 'curtains',        label: 'Curtains',        emoji: '🪟' },
    { key: 'exhaust_fan',     label: 'Exhaust Fan',     emoji: '💨' },
    { key: 'light_fixtures',  label: 'Light Fixtures',  emoji: '💡' },
    { key: 'drawing_room',    label: 'Drawing Room',    emoji: '🛋️' },
    { key: 'store_room',      label: 'Store Room',      emoji: '📦' },
    { key: 'servant_room',    label: 'Servant Room',    emoji: '🚿' },
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
    { key: 'power_backup',  label: 'Power Backup',   emoji: '⚡' },
    { key: 'security',      label: 'Security Guard', emoji: '👮' },
    { key: 'gym',           label: 'Gym Access',     emoji: '💪' },
    { key: 'study_room',    label: 'Study Room',     emoji: '📚' },
  ];

  var PLOT_FACING_OPTIONS = [
    ['', 'Select'], ['east', 'East'], ['west', 'West'],
    ['north', 'North'], ['south', 'South'],
    ['north_east', 'North-East'], ['north_west', 'North-West'],
    ['south_east', 'South-East'], ['south_west', 'South-West'],
    ['corner', 'Corner Plot'], ['three_sides_open', 'Three Sides Open'],
  ];

  var ROAD_FACING_OPTIONS = [
    ['', 'Select'],
    ['10ft', '10 ft'], ['20ft', '20 ft'], ['30ft', '30 ft'],
    ['40ft', '40 ft'], ['60ft', '60 ft'], ['80ft', '80 ft'],
    ['100ft', '100 ft+'],
  ];

  var AREA_UNIT_OPTIONS = [
    ['sqft', 'Sq Ft'], ['sqyard', 'Sq Yards'], ['sqmeter', 'Sq Meter'],
    ['acres', 'Acres'], ['marlas', 'Marlas'], ['bigha', 'Bigha'],
    ['biswa', 'Biswa'], ['cents', 'Cents'],
  ];

  var WATER_SOURCE_OPTIONS = [
    ['', 'Select'], ['borewell', 'Borewell'], ['municipal', 'Municipal / Corporation'],
    ['both', 'Both'], ['well', 'Open Well'], ['tanker', 'Tanker'],
  ];

  var OVERLOOKING = [
    { key: 'garden',      label: 'Garden / Park', emoji: '🌳' },
    { key: 'main_road',   label: 'Main Road',     emoji: '🛣️' },
    { key: 'pool',        label: 'Pool',          emoji: '🏊' },
    { key: 'club',        label: 'Clubhouse',     emoji: '🏛️' },
    { key: 'other_units', label: 'Other Units',   emoji: '🏢' },
  ];

  return {
    RESIDENTIAL_SUBTYPES:  RESIDENTIAL_SUBTYPES,
    COMMERCIAL_SUBTYPES:   COMMERCIAL_SUBTYPES,
    PLOT_TYPES:            PLOT_TYPES,
    FLOOR_TYPES:           FLOOR_TYPES,
    MULTI_FLOOR_TYPES:     MULTI_FLOOR_TYPES,
    AMENITIES:             AMENITIES,
    COMMERCIAL_AMENITIES:  COMMERCIAL_AMENITIES,
    FURNISHING_ITEMS:      FURNISHING_ITEMS,
    PG_AMENITIES:          PG_AMENITIES,
    PLOT_FACING_OPTIONS:   PLOT_FACING_OPTIONS,
    ROAD_FACING_OPTIONS:   ROAD_FACING_OPTIONS,
    AREA_UNIT_OPTIONS:     AREA_UNIT_OPTIONS,
    WATER_SOURCE_OPTIONS:  WATER_SOURCE_OPTIONS,
    OVERLOOKING:           OVERLOOKING,
  };
})();