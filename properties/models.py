from django.db import models
from django.conf import settings
from django.urls import reverse


class Property(models.Model):
    LISTING_TYPE_CHOICES = [
        ('rent', 'For Rent'),
        ('sell', 'For Sale'),
    ]

    PROPERTY_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('villa', 'Villa'),
        ('studio', 'Studio'),
        ('commercial', 'Commercial'),
        ('land', 'Land'),
    ]

    PROPERTY_CATEGORY_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
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

    # ── CORE FIELDS (existing) ──
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=200, help_text='City, Area or Full Address')
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    area_sqft = models.PositiveIntegerField(null=True, blank=True, verbose_name='Area (sq ft)')
    is_furnished = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ── NEW FIELDS ──
    address = models.CharField(max_length=300, blank=True, help_text='Full street address')
    property_category = models.CharField(max_length=20, choices=PROPERTY_CATEGORY_CHOICES, blank=True)
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
    amenities = models.JSONField(default=list, blank=True)
    min_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

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
    def formatted_price(self):
        if self.listing_type == 'rent':
            return f"₹{self.price:,.0f}/mo"
        return f"₹{self.price:,.0f}"


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

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='inquiries'
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='sent_inquiries'
    )
    seeker_name = models.CharField(max_length=100)
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
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]

    inquiry = models.ForeignKey(
        Inquiry,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    sender_role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender_role} reply on {self.inquiry}"
    is_rented = models.BooleanField(default=False)