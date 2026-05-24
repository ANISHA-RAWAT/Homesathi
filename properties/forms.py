from django import forms
from .models import Property, PropertyImage, Inquiry, Review

# ── FURNISHING ITEMS ──────────────────────────────────────────────────────────
# Synced with pp-data.js → FURNISHING_ITEMS
FURNISHING_ITEM_CHOICES = [
    ('bed',             'Bed'),
    ('wardrobe',        'Wardrobe'),
    ('sofa',            'Sofa'),
    ('dining_table',    'Dining Table'),
    ('modular_kitchen', 'Modular Kitchen'),
    ('ac',              'AC'),
    ('fan',             'Fan'),
    ('geyser',          'Geyser'),
    ('water_purifier',  'Water Purifier'),
    ('fridge',          'Refrigerator'),
    ('washing_machine', 'Washing Machine'),
    ('tv',              'TV'),
    ('microwave',       'Microwave'),
    ('chimney',         'Chimney'),
    ('stove',           'Stove / Hob'),
    ('curtains',        'Curtains'),
    ('exhaust_fan',     'Exhaust Fan'),
    ('light_fixtures',  'Light Fixtures'),
    # Added in pp-data.js — were missing before
    ('drawing_room',    'Drawing Room'),
    ('store_room',      'Store Room'),
    ('servant_room',    'Servant Room'),
]

# ── AMENITIES (residential) ───────────────────────────────────────────────────
# Synced with pp-data.js → AMENITIES
AMENITY_CHOICES = [
    ('lift',                 'Lift'),
    ('park',                 'Park'),
    ('gym',                  'Gym'),
    ('power_backup',         'Power Backup'),
    ('clubhouse',            'Clubhouse'),
    ('parking',              'Parking'),
    ('gas_pipeline',         'Gas Pipeline'),
    ('swimming_pool',        'Swimming Pool'),
    ('security_guards',      'Security Guards'),
    ('cctv',                 'CCTV'),
    ('intercom',             'Intercom'),
    ('rainwater_harvesting', 'Rainwater Harvesting'),
    # Builder plot / owner plot amenities (pp-form-owner.js furnishingPanel isPlot=True)
    ('street_lights',  'Street Lights'),
    ('sewage',         'Sewage / Drainage'),
    ('gated',          'Gated Colony'),
    ('security',       'Security Guard'),
    ('playground',     'Playground'),
    # Builder township amenities (pp-form-builder.js amenitiesPanel isPlot=True)
    ('water_supply',   'Water Supply'),
    ('club',           'Club House'),
    ('shopping',       'Shopping Area'),
]

# ── COMMERCIAL AMENITIES ──────────────────────────────────────────────────────
# Synced with pp-data.js → COMMERCIAL_AMENITIES
COMMERCIAL_AMENITY_CHOICES = [
    ('power_backup',    'Power Backup'),
    ('lift',            'Lift'),
    ('parking',         'Parking'),
    ('cctv',            'CCTV'),
    ('security_guards', 'Security Guards'),
    ('fire_safety',     'Fire Safety'),
    ('wifi',            'Wi-Fi'),
    ('cafeteria',       'Cafeteria'),
    ('reception',       'Reception Area'),
    ('conference_room', 'Conference Room'),
    ('ac',              'Central AC'),
    ('washroom',        'Washroom'),
]

# Combined amenity choices: all valid keys from both residential + commercial
ALL_AMENITY_CHOICES = list({k: v for k, v in (
    AMENITY_CHOICES +
    COMMERCIAL_AMENITY_CHOICES +
    [
        ('electricity',      'Electricity Available'),
        ('water_connection', 'Water Connection'),
        ('sewer_connection', 'Sewer Connection'),
        ('borewell',         'Borewell'),
        ('clear_title',      'Clear Title'),
        ('loan_approved',    'Loan Approved'),
        ('registry_ready',   'Registry Ready'),
    ]
)}.items())

# ── OVERLOOKING ───────────────────────────────────────────────────────────────
OVERLOOKING_CHOICES = [
    ('garden',      'Garden / Park'),
    ('main_road',   'Main Road'),
    ('pool',        'Swimming Pool'),
    ('club',        'Club / Amenities'),
    ('other_units', 'Other Units'),
]

# ── PG AMENITIES (pg_amenities chip in pp-form-pg.js) ────────────────────────
PG_AMENITY_CHOICES = [
    ('wifi',          'Wi-Fi'),
    ('ac_room',       'AC Room'),
    ('attached_bath', 'Attached Bath'),
    ('tv',            'TV'),
    ('fridge',        'Refrigerator'),
    ('laundry',       'Laundry'),
    ('meals',         'Meals Included'),
    ('housekeeping',  'Housekeeping'),
    ('cctv',          'CCTV'),
    ('parking',       'Parking'),
    ('power_backup',  'Power Backup'),
    ('security',      'Security Guard'),
    ('gym',           'Gym Access'),
    ('study_room',    'Study Room'),
]

# ── PG COMMON AREAS (common_areas chip in pp-form-pg.js) ─────────────────────
PG_COMMON_AREA_CHOICES = [
    ('wifi',           'Wi-Fi'),
    ('ac_room',        'AC Room'),
    ('attached_bath',  'Attached Bathroom'),
    ('tv',             'TV'),
    ('fridge',         'Refrigerator'),
    ('laundry',        'Laundry'),
    ('meals',          'Meals Included'),
    ('housekeeping',   'Housekeeping'),
    ('cctv',           'CCTV'),
    ('parking',        'Parking'),
    # pp-form-pg.js common_areas chip
    ('common_kitchen', 'Common Kitchen'),
    ('dining_area',    'Dining Area'),
    ('tv_lounge',      'TV Lounge'),
    ('terrace',        'Terrace Access'),
    ('garden',         'Garden'),
    ('indoor_games',   'Indoor Games'),
]

# ── UTILITIES (owner/builder plot forms) ──────────────────────────────────────
UTILITY_CHOICES = [
    ('electricity',      'Electricity Available'),
    ('water_connection', 'Water Connection'),
    ('sewer_connection', 'Sewer Connection'),
    ('borewell',         'Borewell'),
]

# ── LEGAL STATUS (owner/builder plot forms) ───────────────────────────────────
LEGAL_STATUS_CHOICES = [
    ('clear_title',    'Clear Title'),
    ('loan_approved',  'Loan Approved'),
    ('registry_ready', 'Registry Ready'),
]

# ── PROPERTY TYPE GROUPINGS (for validation logic) ────────────────────────────
RESIDENTIAL_TYPES = [
    ('', 'Select sub-type'),
    ('flat_apartment',          'Flat / Apartment'),
    ('independent_house_villa', 'Independent House / Villa'),
    ('builder_floor',           'Independent / Builder Floor'),
    ('plot_land_res',           'Plot / Land'),
    ('studio_1rk',              '1 RK / Studio Apartment'),
    ('farmhouse',               'Farmhouse'),
]

COMMERCIAL_TYPES = [
    ('', 'Select sub-type'),
    ('office',          'Office Space'),
    ('retail',          'Retail / Shop'),
    ('plot_land_com',   'Commercial Plot / Land'),
    ('storage',         'Storage / Warehouse'),
    ('dance_studio',    'Dance / Fitness Studio'),
    ('coworking',       'Co-working Space'),
    ('showroom',        'Showroom'),
    ('restaurant_cafe', 'Restaurant / Café'),
]

PLOT_TYPES  = {'plot_land_res', 'plot_land_com'}
FLOOR_TYPES = {'flat_apartment', 'builder_floor', 'studio_1rk', 'office', 'retail', 'coworking', 'showroom'}


# ═════════════════════════════════════════════════════════════════════════════
#  PROPERTY FORM
# ═════════════════════════════════════════════════════════════════════════════
class PropertyForm(forms.ModelForm):
    # Multi-select JSON fields — use MultipleChoiceField with ALL valid keys
    amenities = forms.MultipleChoiceField(
        choices=ALL_AMENITY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    furnishing_items = forms.MultipleChoiceField(
        choices=FURNISHING_ITEM_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    overlooking = forms.MultipleChoiceField(
        choices=OVERLOOKING_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    pg_common_areas = forms.MultipleChoiceField(
        choices=PG_COMMON_AREA_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Property
        fields = [
            # identity
            'seller_type', 'property_category', 'property_type',
            'listing_type', 'title', 'description',
            # price
            'price', 'min_price', 'max_price',
            # location
            'city', 'state', 'location', 'address',
            # specs
            'bhk', 'bedrooms', 'bathrooms',
            'area_sqft', 'min_area', 'max_area', 'area_unit',
            'construction_status', 'posted_by', 'purchase_type',
            'furnishing', 'is_furnished', 'property_age', 'preferred_tenants',
            # detail fields
            'floor_number', 'total_floors',
            'facing', 'overlooking', 'transaction_type', 'property_ownership',
            'flooring', 'width_of_facing_road', 'water_source',
            'key_highlights', 'key_facilities', 'vastu_compliant',
            'furnishing_items', 'amenities',
            # pg specific
            'pg_for', 'pg_meals_included', 'pg_notice_period', 'pg_common_areas',
            # builder specific
            'project_name', 'rera_id', 'total_units',
        ]
        widgets = {
            'title':               forms.TextInput(attrs={'placeholder': 'e.g. Spacious 3BHK near Metro, Ludhiana'}),
            'description':         forms.Textarea(attrs={'rows': 4}),
            'price':               forms.NumberInput(attrs={'placeholder': 'e.g. 15000'}),
            'min_price':           forms.NumberInput(attrs={'placeholder': 'Min ₹'}),
            'max_price':           forms.NumberInput(attrs={'placeholder': 'Max ₹'}),
            'city':                forms.TextInput(attrs={'placeholder': 'e.g. Ludhiana'}),
            'state':               forms.TextInput(attrs={'placeholder': 'e.g. Punjab'}),
            'location':            forms.TextInput(attrs={'placeholder': 'Locality / Area'}),
            'address':             forms.TextInput(attrs={'placeholder': 'Street / House No.'}),
            'bedrooms':            forms.NumberInput(attrs={'placeholder': '0', 'min': '0'}),
            'bathrooms':           forms.NumberInput(attrs={'placeholder': '0', 'min': '0'}),
            'area_sqft':           forms.NumberInput(attrs={'placeholder': 'e.g. 1200'}),
            'min_area':            forms.NumberInput(attrs={'placeholder': 'Min'}),
            'max_area':            forms.NumberInput(attrs={'placeholder': 'Max'}),
            'floor_number':        forms.TextInput(attrs={'placeholder': 'e.g. 3 or Ground'}),
            'total_floors':        forms.NumberInput(attrs={'placeholder': 'Total floors'}),
            'width_of_facing_road': forms.TextInput(attrs={'placeholder': 'e.g. 30 ft'}),
            'key_highlights':      forms.Textarea(attrs={'rows': 3}),
            'key_facilities':      forms.TextInput(attrs={'placeholder': 'e.g. 24hr Security, CCTV'}),
            'project_name':        forms.TextInput(attrs={'placeholder': 'Builder project / society name'}),
            'rera_id':             forms.TextInput(attrs={'placeholder': 'RERA registration number'}),
            'total_units':         forms.NumberInput(attrs={'placeholder': 'Total units in project'}),
            'pg_notice_period':    forms.TextInput(attrs={'placeholder': 'e.g. 30 days'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_fields = ['title', 'price', 'city', 'description']
        for name, field in self.fields.items():
            field.required = name in required_fields

        for wf in ('listing_type', 'property_category', 'property_type', 'seller_type'):
            if wf in self.fields:
                self.fields[wf].required = False

        self.fields['property_category'].choices = [
            ('', '— Select —'),
            ('residential', 'Residential'),
            ('commercial',  'Commercial'),
            ('pg',          'PG / Co-living'),
        ]

        self.fields['property_type'].choices = (
            [('', '— Select —')] +
            RESIDENTIAL_TYPES[1:] +
            COMMERCIAL_TYPES[1:] +
            [('pg_hostel', 'PG / Hostel')]
        )

        if self.instance and self.instance.pk:
            for field_name in ('amenities', 'furnishing_items', 'overlooking', 'pg_common_areas'):
                val = getattr(self.instance, field_name, [])
                if val:
                    self.initial[field_name] = val

    # ── SAFE CLEAN METHODS ────────────────────────────────────────────────────
    # These silently drop unknown/stale keys instead of raising a validation
    # error. This is the key fix: Django's MultipleChoiceField normally hard-
    # fails if ANY submitted value is not in its choices list. Our JS forms
    # send different chip keys depending on property type (plot amenities are
    # different from residential amenities, etc.), so we must filter instead
    # of reject.

    def clean_amenities(self):
        valid = {k for k, _ in ALL_AMENITY_CHOICES}
        return [v for v in self.data.getlist('amenities') if v in valid]

    def clean_furnishing_items(self):
        valid = {k for k, _ in FURNISHING_ITEM_CHOICES}
        return [v for v in self.data.getlist('furnishing_items') if v in valid]

    def clean_overlooking(self):
        valid = {k for k, _ in OVERLOOKING_CHOICES}
        return [v for v in self.data.getlist('overlooking') if v in valid]

    def clean_pg_common_areas(self):
        # Accepts both pg_common_areas (PG panel) and common_areas (pp-form-pg.js)
        valid = {k for k, _ in PG_COMMON_AREA_CHOICES}
        values = self.data.getlist('pg_common_areas') + self.data.getlist('common_areas')
        return list({v for v in values if v in valid})

    def save(self, commit=True):
        instance = super().save(commit=False)
        for field_name in ('amenities', 'furnishing_items', 'overlooking', 'pg_common_areas'):
            setattr(instance, field_name, self.cleaned_data.get(field_name, []))
        if commit:
            instance.save()
        return instance


# ── IMAGE FORM ────────────────────────────────────────────────────────────────
class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'caption']
        widgets = {
            'image':   forms.FileInput(attrs={'accept': 'image/*'}),
            'caption': forms.TextInput(attrs={'placeholder': 'Optional caption'}),
        }


PropertyImageFormSet = forms.inlineformset_factory(
    Property, PropertyImage,
    form=PropertyImageForm,
    extra=5, max_num=15, can_delete=True
)


# ── INQUIRY FORM ──────────────────────────────────────────────────────────────
class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['seeker_name', 'seeker_email', 'seeker_phone', 'message']
        widgets = {
            'seeker_name':  forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your full name'}),
            'seeker_email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Your email address'}),
            'seeker_phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number (optional)'}),
            'message':      forms.Textarea(attrs={'class': 'form-input', 'rows': 4,
                            'placeholder': "Tell the owner about yourself and when you'd like to visit…"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and self.user.is_authenticated:
            self.fields['seeker_email'].required = False
            self.fields['seeker_email'].widget.attrs['placeholder'] = self.user.email
        else:
            self.fields['seeker_email'].required = True


# ── REPLY FORM ────────────────────────────────────────────────────────────────
class ReplyForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-input', 'rows': 3, 'placeholder': 'Write your reply…'
        })
    )


# ── SEARCH FORM ───────────────────────────────────────────────────────────────
class SearchForm(forms.Form):
    LISTING_TYPE_CHOICES  = [('', 'Any Type')]  + Property.LISTING_TYPE_CHOICES
    PROPERTY_TYPE_CHOICES = [('', 'Any Property')] + Property.PROPERTY_TYPE_CHOICES

    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input search-input',
            'placeholder': 'Search by city, location or area…'
        })
    )
    listing_type = forms.ChoiceField(
        choices=LISTING_TYPE_CHOICES, required=False,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    property_type = forms.ChoiceField(
        choices=PROPERTY_TYPE_CHOICES, required=False,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    min_price = forms.DecimalField(
        required=False, min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Min ₹'})
    )
    max_price = forms.DecimalField(
        required=False, min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Max ₹'})
    )
    bedrooms = forms.IntegerField(
        required=False, min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Min Bedrooms'})
    )
    furnishing = forms.ChoiceField(
        choices=[('', 'Any Furnishing')] + Property.FURNISHING_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'})
    )


# ── REVIEW FORM ───────────────────────────────────────────────────────────────
class ReviewForm(forms.ModelForm):
    STAR_CHOICES = [('', '— Select —')] + [(str(i), f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)]

    property_rating = forms.ChoiceField(
        choices=STAR_CHOICES, label='Property Rating',
        widget=forms.Select(attrs={'class': 'form-input review-star-select', 'id': 'id_property_rating'}),
    )
    owner_rating = forms.ChoiceField(
        choices=STAR_CHOICES, label='Owner Rating',
        widget=forms.Select(attrs={'class': 'form-input review-star-select', 'id': 'id_owner_rating'}),
    )

    class Meta:
        model = Review
        fields = ['property_rating', 'owner_rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-input', 'rows': 4,
                'placeholder': 'Share your experience — Was the property as described? How was the owner to deal with?',
            }),
        }

    def clean_property_rating(self):
        val = self.cleaned_data.get('property_rating')
        if not val:
            raise forms.ValidationError('Please select a property rating.')
        val = int(val)
        if not (1 <= val <= 5):
            raise forms.ValidationError('Rating must be between 1 and 5.')
        return val

    def clean_owner_rating(self):
        val = self.cleaned_data.get('owner_rating')
        if not val:
            raise forms.ValidationError('Please select an owner rating.')
        val = int(val)
        if not (1 <= val <= 5):
            raise forms.ValidationError('Rating must be between 1 and 5.')
        return val