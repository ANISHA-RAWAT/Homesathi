from django import forms
from .models import Property, PropertyImage, Inquiry, Review

# ── FURNISHING ITEMS ──────────────────────────────────────────────────────────
FURNISHING_ITEM_CHOICES = [
    ('water_purifier', 'Water Purifier'),
    ('fan', 'Fan'),
    ('exhaust_fan', 'Exhaust Fan'),
    ('dining_table', 'Dining Table'),
    ('geyser', 'Geyser'),
    ('light', 'Light'),
    ('modular_kitchen', 'Modular Kitchen'),
    ('curtains', 'Curtains'),
    ('bed', 'Bed'),
    ('wardrobe', 'Wardrobe'),
    ('sofa', 'Sofa'),
    ('microwave', 'Microwave'),
    ('ac', 'AC'),
    ('chimney', 'Chimney'),
    ('fridge', 'Refrigerator'),
    ('stove', 'Stove'),
    ('tv', 'TV'),
    ('washing_machine', 'Washing Machine'),
]

AMENITY_CHOICES = [
    ('lift', 'Lift'),
    ('park', 'Park'),
    ('gym', 'Gym'),
    ('power_backup', 'Power Backup'),
    ('clubhouse', 'Clubhouse'),
    ('parking', 'Parking'),
    ('gas_pipeline', 'Gas Pipeline'),
    ('swimming_pool', 'Swimming Pool'),
    ('security_guards', 'Security Guards'),
    ('cctv', 'CCTV'),
    ('intercom', 'Intercom'),
    ('rainwater_harvesting', 'Rainwater Harvesting'),
]

OVERLOOKING_CHOICES = [
    ('garden', 'Garden / Park'),
    ('main_road', 'Main Road'),
    ('pool', 'Swimming Pool'),
    ('club', 'Club / Amenities'),
    ('other_units', 'Other Units'),
]

PG_COMMON_AREA_CHOICES = [
    ('wifi', 'Wi-Fi'),
    ('ac_room', 'AC Room'),
    ('attached_bath', 'Attached Bathroom'),
    ('tv', 'TV'),
    ('fridge', 'Refrigerator'),
    ('laundry', 'Laundry'),
    ('meals', 'Meals Included'),
    ('housekeeping', 'Housekeeping'),
    ('cctv', 'CCTV'),
    ('parking', 'Parking'),
]

RESIDENTIAL_TYPES = [
    ('', 'Select sub-type'),
    ('flat_apartment', 'Flat / Apartment'),
    ('independent_house_villa', 'Independent House / Villa'),
    ('builder_floor', 'Independent / Builder Floor'),
    ('plot_land_res', 'Plot / Land'),
    ('studio_1rk', '1 RK / Studio Apartment'),
    ('farmhouse', 'Farmhouse'),
]

COMMERCIAL_TYPES = [
    ('', 'Select sub-type'),
    ('office', 'Office Space'),
    ('retail', 'Retail / Shop'),
    ('plot_land_com', 'Commercial Plot / Land'),
    ('storage', 'Storage / Warehouse'),
    ('dance_studio', 'Dance / Fitness Studio'),
    ('coworking', 'Co-working Space'),
    ('showroom', 'Showroom'),
    ('restaurant_cafe', 'Restaurant / Café'),
]

# Plot/land types — no BHK/floors needed
PLOT_TYPES = {'plot_land_res', 'plot_land_com', 'farmhouse'}
# Types where floor-level fields make sense
FLOOR_TYPES = {'flat_apartment', 'builder_floor', 'studio_1rk', 'office', 'retail', 'coworking', 'showroom'}


class PropertyForm(forms.ModelForm):
    amenities = forms.MultipleChoiceField(
        choices=AMENITY_CHOICES,
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
            # new fields
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
            'description':         forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the property, locality highlights, nearby landmarks…'}),
            'price':               forms.NumberInput(attrs={'placeholder': 'e.g. 15000'}),
            'min_price':           forms.NumberInput(attrs={'placeholder': 'Min ₹'}),
            'max_price':           forms.NumberInput(attrs={'placeholder': 'Max ₹'}),
            'city':                forms.TextInput(attrs={'placeholder': 'e.g. Ludhiana'}),
            'state':               forms.TextInput(attrs={'placeholder': 'e.g. Punjab'}),
            'location':            forms.TextInput(attrs={'placeholder': 'Locality / Area, e.g. Model Town'}),
            'address':             forms.TextInput(attrs={'placeholder': 'Street / House No.'}),
            'bedrooms':            forms.NumberInput(attrs={'placeholder': '0', 'min': '0'}),
            'bathrooms':           forms.NumberInput(attrs={'placeholder': '0', 'min': '0'}),
            'area_sqft':           forms.NumberInput(attrs={'placeholder': 'e.g. 1200'}),
            'min_area':            forms.NumberInput(attrs={'placeholder': 'Min'}),
            'max_area':            forms.NumberInput(attrs={'placeholder': 'Max'}),
            'floor_number':        forms.TextInput(attrs={'placeholder': 'e.g. 3 or Ground'}),
            'total_floors':        forms.NumberInput(attrs={'placeholder': 'Total floors in building'}),
            'width_of_facing_road': forms.TextInput(attrs={'placeholder': 'e.g. 30 ft or 9 metres'}),
            'key_highlights':      forms.Textarea(attrs={'rows': 3, 'placeholder': 'e.g. Corner unit, park-facing, recently renovated…'}),
            'key_facilities':      forms.TextInput(attrs={'placeholder': 'e.g. 24hr Security, CCTV, Visitor Parking'}),
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
            ('commercial', 'Commercial'),
            ('pg', 'PG / Co-living'),
        ]

        self.fields['property_type'].choices = (
            [('', '— Select —')] +
            RESIDENTIAL_TYPES[1:] +
            COMMERCIAL_TYPES[1:] +
            [('pg_hostel', 'PG / Hostel')]
        )

        if self.instance and self.instance.pk:
            for field in ('amenities', 'furnishing_items', 'overlooking', 'pg_common_areas'):
                val = getattr(self.instance, field, [])
                if val:
                    self.initial[field] = val

    def save(self, commit=True):
        instance = super().save(commit=False)
        for field in ('amenities', 'furnishing_items', 'overlooking', 'pg_common_areas'):
            setattr(instance, field, self.cleaned_data.get(field, []))
        if commit:
            instance.save()
        return instance


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


class ReplyForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Write your reply…'})
    )


class SearchForm(forms.Form):
    LISTING_TYPE_CHOICES = [('', 'Any Type')] + Property.LISTING_TYPE_CHOICES
    PROPERTY_TYPE_CHOICES = [('', 'Any Property')] + Property.PROPERTY_TYPE_CHOICES

    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input search-input',
                                      'placeholder': 'Search by city, location or area…'})
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


class ReviewForm(forms.ModelForm):
    """Form for submitting / editing a property review."""
    STAR_CHOICES = [('', '— Select —')] + [(str(i), f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)]

    property_rating = forms.ChoiceField(
        choices=STAR_CHOICES,
        label='Property Rating',
        widget=forms.Select(attrs={'class': 'form-input review-star-select', 'id': 'id_property_rating'}),
    )
    owner_rating = forms.ChoiceField(
        choices=STAR_CHOICES,
        label='Owner Rating',
        widget=forms.Select(attrs={'class': 'form-input review-star-select', 'id': 'id_owner_rating'}),
    )

    class Meta:
        model = Review
        fields = ['property_rating', 'owner_rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4,
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