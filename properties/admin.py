from django.contrib import admin
from .models import Property, PropertyImage, Inquiry, InquiryReply, Review


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


class InquiryReplyInline(admin.TabularInline):
    model = InquiryReply
    extra = 0
    readonly_fields = ('sender', 'sender_role', 'message', 'created_at')
    can_delete = False


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display    = ('title', 'owner', 'listing_type', 'city', 'price', 'status', 'view_count', 'created_at')
    list_filter     = ('listing_type', 'property_type', 'status')
    search_fields   = ('title', 'city', 'owner__email')
    readonly_fields = ('view_count', 'created_at', 'updated_at')
    inlines         = [PropertyImageInline]


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display    = ('seeker_name', 'seeker_email', 'seeker_phone', 'property', 'buyer', 'status', 'created_at')
    list_filter     = ('status', 'created_at')
    search_fields   = ('seeker_name', 'seeker_email', 'seeker_phone', 'property__title', 'buyer__email')
    readonly_fields = ('seeker_name', 'seeker_email', 'seeker_phone', 'message', 'buyer', 'property', 'created_at')
    inlines         = [InquiryReplyInline]


# ── Custom list filter: Site-wide vs Property review ──────────────────────────
class ReviewTypeFilter(admin.SimpleListFilter):
    title           = 'Review Type'
    parameter_name  = 'review_type'

    def lookups(self, request, model_admin):
        return [
            ('sitewide', '🌐 Site-wide (needs approval)'),
            ('property', '🏠 Property (auto-approved)'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'sitewide':
            return queryset.filter(related_property__isnull=True)
        if self.value() == 'property':
            return queryset.filter(related_property__isnull=False)
        return queryset


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display    = (
        'reviewer',
        'review_type',
        'related_property',
        'property_rating',
        'owner_rating',
        'short_comment',
        'is_approved',
        'created_at',
    )
    list_filter     = (ReviewTypeFilter, 'is_approved', 'property_rating')
    search_fields   = ('reviewer__email', 'comment', 'related_property__title')
    list_editable   = ('is_approved',)
    readonly_fields = ('reviewer', 'related_property', 'property_rating', 'owner_rating', 'comment', 'created_at')
    ordering        = ('-created_at',)

    actions = ['approve_reviews', 'reject_reviews']

    @admin.display(description='Type')
    def review_type(self, obj):
        if obj.related_property_id:
            return '🏠 Property'
        return '🌐 Site-wide'

    @admin.display(description='Comment')
    def short_comment(self, obj):
        if obj.comment:
            return obj.comment[:70] + ('...' if len(obj.comment) > 70 else '')
        return '-'

    @admin.action(description='✅ Approve selected reviews')
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} review(s) approved and now visible on site.')

    @admin.action(description='❌ Reject / Hide selected reviews')
    def reject_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} review(s) hidden from site.')