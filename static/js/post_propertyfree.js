document.addEventListener('DOMContentLoaded', function () {

    // ── DECLARE EVERYTHING FIRST ───────────────────────────────────────────────

    // Only NON-REQUIRED fields are disabled for Land.
    // Required fields (title, listing_type, price, city) stay enabled always.
    // Locality (id_location) and Address (id_address) also stay enabled always.

    var DISABLE_IDS = [
        "id_bhk",
        "id_construction_status",
        "id_posted_by",
        "id_min_area", "id_max_area", "id_area_unit",
        "id_purchase_type",
        "id_furnishing",
        "id_property_age",
        "id_preferred_tenants",
        "property_video",
        "id_description"
    ];

    var DISABLE_NAMES = ["amenities"];

    function setLandMode(isLand) {
        // disable/enable by id
        DISABLE_IDS.forEach(function (id) {
            var el = document.getElementById(id);
            if (el) el.disabled = isLand;
        });

        // disable/enable amenities checkboxes by name
        DISABLE_NAMES.forEach(function (name) {
            document.querySelectorAll('[name="' + name + '"]').forEach(function (el) {
                el.disabled = isLand;
            });
        });

        // visual dimming on parent .form-section
        DISABLE_IDS.forEach(function (id) {
            var el = document.getElementById(id);
            if (!el) return;
            var section = el.closest('.form-section');
            if (section) {
                section.style.opacity       = isLand ? '0.4' : '1';
                section.style.pointerEvents = isLand ? 'none' : '';
            }
        });

        DISABLE_NAMES.forEach(function (name) {
            var el = document.querySelector('[name="' + name + '"]');
            if (!el) return;
            var section = el.closest('.form-section');
            if (section) {
                section.style.opacity       = isLand ? '0.4' : '1';
                section.style.pointerEvents = isLand ? 'none' : '';
            }
        });

        // images required only when not land
        var imagesInput = document.getElementById("property_images");
        if (imagesInput) imagesInput.required = !isLand;
    }

    // ── PROPERTY CATEGORY / TYPE ───────────────────────────────────────────────

    var category     = document.getElementById("id_property_category");
    var propertyType = document.getElementById("id_property_type");

    var residentialOptions = [
        { value: "apartment", label: "Apartment" },
        { value: "house",     label: "House" },
        { value: "villa",     label: "Villa" },
        { value: "studio",    label: "Studio" }
    ];

    var commercialOptions = [
        { value: "commercial", label: "Commercial" },
        { value: "land",       label: "Land" }
    ];

    if (category && propertyType) {
        category.addEventListener("change", function () {
            propertyType.innerHTML = '<option value="">Select Property Type</option>';
            var list = this.value === "residential" ? residentialOptions : commercialOptions;
            list.forEach(function (item) {
                var opt = document.createElement("option");
                opt.value       = item.value;
                opt.textContent = item.label;
                propertyType.appendChild(opt);
            });
            setLandMode(false);
        });

        propertyType.addEventListener("change", function () {
            setLandMode(this.value === "land");
        });

        // Run once on page load
        setLandMode(propertyType.value === "land");
    }

    // ── IMAGE REQUIRED VALIDATION ──────────────────────────────────────────────

    var imagesInput = document.getElementById("property_images");

    if (imagesInput && !document.getElementById("images-error")) {
        var errSpan = document.createElement("span");
        errSpan.id = "images-error";
        errSpan.style.cssText = "color:red;font-size:13px;display:none;margin-top:4px;";
        errSpan.textContent = "Please upload at least one photo.";
        imagesInput.insertAdjacentElement("afterend", errSpan);

        imagesInput.addEventListener("change", function () {
            if (this.files && this.files.length > 0) {
                errSpan.style.display = "none";
            }
        });
    }

    var form = document.getElementById("propertyForm");
    if (form) {
        form.addEventListener("submit", function (e) {
            var img     = document.getElementById("property_images");
            var errSpan = document.getElementById("images-error");
            if (!img || img.disabled) return;

            if (!img.files || img.files.length === 0) {
                e.preventDefault();
                if (errSpan) errSpan.style.display = "block";
                img.scrollIntoView({ behavior: "smooth", block: "center" });
            }
        });
    }

});