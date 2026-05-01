from django.contrib import admin
from .models import Property, PropertyImage, Inquiry, InquiryReply


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
    list_display = ('title', 'owner', 'listing_type', 'city', 'price', 'status', 'view_count', 'created_at')
    list_filter = ('listing_type', 'property_type', 'status')
    search_fields = ('title', 'city', 'owner__email')
    readonly_fields = ('view_count', 'created_at', 'updated_at')
    inlines = [PropertyImageInline]


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display  = ('seeker_name', 'seeker_email', 'seeker_phone', 'property', 'buyer', 'status', 'created_at')
    list_filter   = ('status', 'created_at')
    search_fields = ('seeker_name', 'seeker_email', 'seeker_phone', 'property__title', 'buyer__email')
    readonly_fields = ('seeker_name', 'seeker_email', 'seeker_phone', 'message', 'buyer', 'property', 'created_at')
    inlines = [InquiryReplyInline]

from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'rating', 'is_approved', 'created_at')
    list_filter   = ('is_approved', 'rating')
    search_fields = ('name', 'email', 'message')
    list_editable = ('is_approved',)
    readonly_fields = ('name', 'email', 'rating', 'message', 'created_at')
    actions = ['approve_reviews', 'reject_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} review(s) approved.")
    approve_reviews.short_description = "Approve selected reviews"

    def reject_reviews(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f"{queryset.count()} review(s) rejected.")
    reject_reviews.short_description = "Reject selected reviews"