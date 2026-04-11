from django import forms
from .models import Property, PropertyImage, Inquiry

RESIDENTIAL_TYPES = [
    ('', 'Select Property Type'),
    ('apartment', 'Apartment'),
    ('house', 'House'),
    ('villa', 'Villa'),
    ('studio', '1 RK / Studio Apartment'),
]

COMMERCIAL_TYPES = [
    ('', 'Select Property Type'),
    ('office', 'Office'),
    ('retail', 'Retail / Shop'),
    ('plot', 'Plot / Land'),
    ('storage', 'Storage / Warehouse'),
    ('work_live_studio', 'Work-Live Studio'),
]

ALL_TYPES = RESIDENTIAL_TYPES + COMMERCIAL_TYPES[1:]


class PropertyForm(forms.ModelForm):
    AMENITY_CHOICES = [
        ('Lift', 'Lift'),
        ('Park', 'Park'),
        ('Gym', 'Gym'),
        ('Power Backup', 'Power Backup'),
        ('Clubhouse', 'Clubhouse'),
        ('Parking', 'Parking'),
        ('Gas Pipeline', 'Gas Pipeline'),
        ('Swimming Pool', 'Swimming Pool'),
        ('Security Guards', 'Security Guards'),
    ]
    amenities = forms.MultipleChoiceField(
        choices=AMENITY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Property
        fields = [
            'title', 'listing_type', 'property_category', 'property_type',
            'price', 'min_price', 'max_price',
            'city', 'state', 'location', 'address',
            'bhk', 'bedrooms', 'bathrooms',
            'min_area', 'max_area', 'area_unit', 'area_sqft',
            'construction_status', 'posted_by', 'purchase_type',
            'furnishing', 'is_furnished', 'property_age',
            'preferred_tenants', 'amenities', 'description',
        ]
        widgets = {
            'title':       forms.TextInput(attrs={'placeholder': 'e.g. 2BHK Apartment in Ludhiana'}),
            'price':       forms.NumberInput(attrs={'placeholder': 'e.g. 15000'}),
            'min_price':   forms.NumberInput(attrs={'placeholder': 'Minimum Price'}),
            'max_price':   forms.NumberInput(attrs={'placeholder': 'Maximum Price'}),
            'city':        forms.TextInput(attrs={'placeholder': 'e.g. Ludhiana'}),
            'state':       forms.TextInput(attrs={'placeholder': 'e.g. Punjab'}),
            'location':    forms.TextInput(attrs={'placeholder': 'Area / Locality'}),
            'address':     forms.TextInput(attrs={'placeholder': 'e.g. House No. 12, Street 4, Model Town'}),
            'bedrooms':    forms.NumberInput(attrs={'placeholder': 'e.g. 2'}),
            'bathrooms':   forms.NumberInput(attrs={'placeholder': 'e.g. 2'}),
            'area_sqft':   forms.NumberInput(attrs={'placeholder': 'e.g. 1200'}),
            'min_area':    forms.NumberInput(attrs={'placeholder': 'Min Area'}),
            'max_area':    forms.NumberInput(attrs={'placeholder': 'Max Area'}),
            'description': forms.Textarea(attrs={'placeholder': 'Write about locality, schools, hospitals, highway access etc', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Required fields
        required_fields = ['title', 'listing_type', 'property_category', 'property_type', 'price', 'city', 'description']
        for field_name, field in self.fields.items():
            field.required = field_name in required_fields

        # Category dropdown with blank prompt
        self.fields['property_category'].choices = [
            ('', 'Select Category'),
            ('residential', 'Residential'),
            ('commercial', 'Commercial'),
        ]

        # Dynamic property_type choices based on selected category
        category = None
        if self.data.get('property_category'):
            category = self.data.get('property_category')
        elif self.instance and self.instance.pk:
            category = self.instance.property_category

        if category == 'commercial':
            self.fields['property_type'].choices = COMMERCIAL_TYPES
        elif category == 'residential':
            self.fields['property_type'].choices = RESIDENTIAL_TYPES
        else:
            self.fields['property_type'].choices = [('', 'Select Category First')] + ALL_TYPES[1:]

        # Pre-populate amenities from existing instance
        if self.instance and self.instance.pk and self.instance.amenities:
            self.initial['amenities'] = self.instance.amenities

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.amenities = self.cleaned_data.get('amenities', [])
        if commit:
            instance.save()
        return instance


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'caption']
        widgets = {
            'image':   forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/*'}),
            'caption': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Optional caption'}),
        }


PropertyImageFormSet = forms.inlineformset_factory(
    Property, PropertyImage,
    form=PropertyImageForm,
    extra=3,
    max_num=10,
    can_delete=True
)


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['seeker_name', 'seeker_phone', 'message']
        widgets = {
            'seeker_name':  forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your full name'}),
            'seeker_phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number (optional)'}),
            'message':      forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': "Tell the owner about yourself and when you'd like to visit..."}),
        }


class ReplyForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Write your reply...'})
    )


class SearchForm(forms.Form):
    LISTING_TYPE_CHOICES = [('', 'Any Type')] + Property.LISTING_TYPE_CHOICES
    PROPERTY_TYPE_CHOICES = [('', 'Any Property')] + Property.PROPERTY_TYPE_CHOICES

    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input search-input', 'placeholder': 'Search by city, location or area...'})
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
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Min Price ₹'})
    )
    max_price = forms.DecimalField(
        required=False, min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Max Price ₹'})
    )
    bedrooms = forms.IntegerField(
        required=False, min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Min Bedrooms'})
    )