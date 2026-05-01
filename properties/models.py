from django.db import models
from django.conf import settings
from django.urls import reverse


class Property(models.Model):
    LISTING_TYPE_CHOICES = [
        ('rent', 'For Rent'),
        ('sell', 'For Sale'),
        ('pg', 'PG / Co-living'),
    ]

    PROPERTY_TYPE_CHOICES = [
        # Residential
        ('flat_apartment', 'Flat / Apartment'),
        ('independent_house_villa', 'Independent House / Villa'),
        ('builder_floor', 'Independent / Builder Floor'),
        ('plot_land_res', 'Plot / Land'),
        ('studio_1rk', '1 RK / Studio Apartment'),
        ('farmhouse', 'Farmhouse'),
        # Commercial
        ('office', 'Office Space'),
        ('retail', 'Retail / Shop'),
        ('plot_land_com', 'Commercial Plot / Land'),
        ('storage', 'Storage / Warehouse'),
        ('dance_studio', 'Dance / Fitness Studio'),
        ('coworking', 'Co-working Space'),
        ('showroom', 'Showroom'),
        ('restaurant_cafe', 'Restaurant / Café'),
        # PG
        ('pg_hostel', 'PG / Hostel'),
    ]

    PROPERTY_CATEGORY_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('pg', 'PG / Co-living'),
    ]

    SELLER_TYPE_CHOICES = [
        ('pg_owner', 'PG Owner'),
        ('owner', 'Owner'),
        ('builder', 'Builder'),
        ('dealer', 'Dealer'),
    ]

    BHK_CHOICES = [
        ('1rk', '1 RK'),
        ('1bhk', '1 BHK'),
        ('2bhk', '2 BHK'),
        ('3bhk', '3 BHK'),
        ('4bhk', '4 BHK'),
        ('5bhk+', '5 BHK+'),
    ]

    CONSTRUCTION_STATUS_CHOICES = [
        ('new_launch', 'New Launch'),
        ('under_construction', 'Under Construction'),
        ('ready_to_move', 'Ready To Move'),
    ]

    POSTED_BY_CHOICES = [
        ('owner', 'Owner'),
        ('builder', 'Builder'),
        ('dealer', 'Dealer'),
        ('featured_dealer', 'Featured Dealer'),
    ]

    AREA_UNIT_CHOICES = [
        ('sqft', 'Sq Ft'),
        ('sqyard', 'Sq Yards'),
        ('sqmeter', 'Sq Meter'),
        ('acres', 'Acres'),
        ('marlas', 'Marlas'),
        ('cents', 'Cents'),
    ]

    PURCHASE_TYPE_CHOICES = [
        ('resale', 'Resale'),
        ('new_booking', 'New Booking'),
    ]

    FURNISHING_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]

    PROPERTY_AGE_CHOICES = [
        ('0-1', '0-1 Years'),
        ('1-5', '1-5 Years'),
        ('5-10', '5-10 Years'),
        ('10-20', '10-20 Years'),
        ('20+', '20+ Years'),
    ]

    PREFERRED_TENANTS_CHOICES = [
        ('family', 'Family'),
        ('single_man', 'Single Man'),
        ('single_woman', 'Single Woman'),
        ('company_lease', 'Company Lease'),
        ('any', 'Any'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('sold', 'Sold/Rented'),
    ]

    FACING_CHOICES = [
        ('east', 'East'),
        ('west', 'West'),
        ('north', 'North'),
        ('south', 'South'),
        ('north_east', 'North-East'),
        ('north_west', 'North-West'),
        ('south_east', 'South-East'),
        ('south_west', 'South-West'),
    ]

    OVERLOOKING_CHOICES = [
        ('garden', 'Garden / Park'),
        ('main_road', 'Main Road'),
        ('pool', 'Swimming Pool'),
        ('club', 'Club / Amenities'),
        ('other_units', 'Other Units'),
    ]

    TRANSACTION_TYPE_CHOICES = [
        ('new_property', 'New Property'),
        ('resale', 'Resale'),
    ]

    PROPERTY_OWNERSHIP_CHOICES = [
        ('freehold', 'Freehold'),
        ('leasehold', 'Leasehold'),
        ('cooperative', 'Co-operative Society'),
        ('power_of_attorney', 'Power of Attorney'),
    ]

    FLOORING_CHOICES = [
        ('marble', 'Marble'),
        ('vitrified_tiles', 'Vitrified Tiles'),
        ('ceramic_tiles', 'Ceramic Tiles'),
        ('wooden', 'Wooden'),
        ('granite', 'Granite'),
        ('mosaic', 'Mosaic'),
        ('normal_tiles', 'Normal Tiles'),
    ]

    WATER_SOURCE_CHOICES = [
        ('borewell', 'Borewell'),
        ('municipal', 'Municipal Corporation'),
        ('both', 'Both (Borewell + Municipal)'),
    ]

    # ── CORE FIELDS ──
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    property_type = models.CharField(max_length=30, choices=PROPERTY_TYPE_CHOICES)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=200, help_text='City, Area or Full Address')
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    bedrooms = models.PositiveIntegerField(default=0, null=True, blank=True)
    bathrooms = models.PositiveIntegerField(default=0, null=True, blank=True)
    area_sqft = models.PositiveIntegerField(null=True, blank=True, verbose_name='Area (sq ft)')
    is_furnished = models.BooleanField(default=False)
    is_rented = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ── SELLER / CATEGORY ──
    seller_type = models.CharField(max_length=20, choices=SELLER_TYPE_CHOICES, blank=True)
    property_category = models.CharField(max_length=20, choices=PROPERTY_CATEGORY_CHOICES, blank=True)

    # ── LOCATION DETAIL ──
    address = models.CharField(max_length=300, blank=True)

    # ── PROPERTY SPECS ──
    bhk = models.CharField(max_length=10, choices=BHK_CHOICES, blank=True)
    construction_status = models.CharField(max_length=20, choices=CONSTRUCTION_STATUS_CHOICES, blank=True)
    posted_by = models.CharField(max_length=20, choices=POSTED_BY_CHOICES, blank=True)
    min_area = models.PositiveIntegerField(null=True, blank=True)
    max_area = models.PositiveIntegerField(null=True, blank=True)
    area_unit = models.CharField(max_length=10, choices=AREA_UNIT_CHOICES, default='sqft', blank=True)
    purchase_type = models.CharField(max_length=15, choices=PURCHASE_TYPE_CHOICES, blank=True)
    furnishing = models.CharField(max_length=15, choices=FURNISHING_CHOICES, blank=True)
    property_age = models.CharField(max_length=10, choices=PROPERTY_AGE_CHOICES, blank=True)
    preferred_tenants = models.CharField(max_length=15, choices=PREFERRED_TENANTS_CHOICES, blank=True)
    min_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # ── NEW DETAILED FIELDS ──
    floor_number = models.CharField(max_length=20, blank=True, help_text='e.g. 3, Ground, Basement')
    total_floors = models.PositiveIntegerField(null=True, blank=True)
    facing = models.CharField(max_length=15, choices=FACING_CHOICES, blank=True)
    overlooking = models.JSONField(default=list, blank=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES, blank=True)
    property_ownership = models.CharField(max_length=25, choices=PROPERTY_OWNERSHIP_CHOICES, blank=True)
    flooring = models.CharField(max_length=20, choices=FLOORING_CHOICES, blank=True)
    width_of_facing_road = models.CharField(max_length=30, blank=True, help_text='e.g. 30 ft, 9 metres')
    water_source = models.CharField(max_length=20, choices=WATER_SOURCE_CHOICES, blank=True)
    key_highlights = models.TextField(blank=True, help_text='Why should someone consider this property?')
    key_facilities = models.TextField(blank=True, help_text='Comma-separated facilities, e.g. 24hr Security, CCTV')
    vastu_compliant = models.BooleanField(default=False)

    # ── FURNISHING ITEMS (JSONField list of item keys) ──
    furnishing_items = models.JSONField(default=list, blank=True)

    # ── AMENITIES ──
    amenities = models.JSONField(default=list, blank=True)

    # ── PG-SPECIFIC ──
    pg_for = models.CharField(max_length=20, blank=True,
        choices=[('male','Male'),('female','Female'),('any','Any')])
    pg_meals_included = models.BooleanField(default=False)
    pg_notice_period = models.CharField(max_length=30, blank=True)
    pg_common_areas = models.JSONField(default=list, blank=True)

    # ── BUILDER-SPECIFIC ──
    project_name = models.CharField(max_length=200, blank=True)
    rera_id = models.CharField(max_length=50, blank=True, verbose_name='RERA ID')
    total_units = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Properties'

    def __str__(self):
        return f"{self.title} ({self.get_listing_type_display()})"

    def get_absolute_url(self):
        return reverse('property_detail', kwargs={'pk': self.pk})

    def increment_view(self):
        Property.objects.filter(pk=self.pk).update(view_count=models.F('view_count') + 1)
        self.refresh_from_db(fields=['view_count'])

    @property
    def primary_image(self):
        return self.images.first()

    @property
    def avg_rating(self):
        """Returns average star rating from approved reviews for this property."""
        try:
            from django.db.models import Avg
            # Use global approved reviews average as site-wide rating indicator
            result = Review.objects.filter(is_approved=True).aggregate(avg=Avg('rating'))
            val = result['avg'] or 0
            return round(val, 1)
        except Exception:
            return 0

    def avg_rating_int(self):
        """Returns integer floor of avg_rating for star loop comparisons."""
        return int(self.avg_rating)

    def formatted_price(self):
        price = self.price
        if price >= 10_000_000:
            return f"₹{price/10_000_000:.2f} Cr"
        elif price >= 100_000:
            return f"₹{price/100_000:.2f} L"
        if self.listing_type == 'rent':
            return f"₹{price:,.0f}/mo"
        return f"₹{price:,.0f}"

    @property
    def key_facilities_list(self):
        if not self.key_facilities:
            return []
        return [f.strip() for f in self.key_facilities.split(',') if f.strip()]

    @property
    def furnishing_items_display(self):
        ITEMS = {
            'water_purifier': 'Water Purifier',
            'fan': 'Fan', 'exhaust_fan': 'Exhaust Fan',
            'dining_table': 'Dining Table', 'geyser': 'Geyser',
            'light': 'Light', 'modular_kitchen': 'Modular Kitchen',
            'curtains': 'Curtains', 'bed': 'Bed', 'wardrobe': 'Wardrobe',
            'sofa': 'Sofa', 'microwave': 'Microwave', 'ac': 'AC',
            'chimney': 'Chimney', 'fridge': 'Refrigerator', 'stove': 'Stove',
            'tv': 'TV', 'washing_machine': 'Washing Machine',
        }
        return [ITEMS[k] for k in (self.furnishing_items or []) if k in ITEMS]


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='properties/%Y/%m/')
    caption = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'uploaded_at']

    def __str__(self):
        return f"Image for {self.property.title}"


class Inquiry(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('closed', 'Closed'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='sent_inquiries'
    )
    seeker_name  = models.CharField(max_length=100)
    seeker_email = models.EmailField(blank=True, help_text='Contact email of the seeker')
    seeker_phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        return f"Inquiry from {self.seeker_name} for {self.property.title}"

    def unread_count_for_seller(self):
        return self.replies.filter(sender_role='buyer', is_read=False).count()

    def unread_count_for_buyer(self):
        return self.replies.filter(sender_role='seller', is_read=False).count()


class InquiryReply(models.Model):
    ROLE_CHOICES = [('buyer', 'Buyer'), ('seller', 'Seller')]

    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, related_name='replies')
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    sender_role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender_role} reply on {self.inquiry}"


class Review(models.Model):
    STAR_CHOICES = [(i, i) for i in range(1, 6)]
    name        = models.CharField(max_length=100)
    email       = models.EmailField()
    rating      = models.PositiveSmallIntegerField(choices=STAR_CHOICES)
    message     = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.rating}★ ({'Approved' if self.is_approved else 'Pending'})"