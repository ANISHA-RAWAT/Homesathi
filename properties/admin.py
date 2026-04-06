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
    list_display = ('seeker_name', 'property', 'status', 'created_at')
    list_filter = ('status',)
    readonly_fields = ('seeker_name', 'seeker_phone', 'message', 'buyer', 'created_at')
    inlines = [InquiryReplyInline]