from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponseForbidden

from .models import Property, Inquiry, InquiryReply
from .forms import PropertyForm, PropertyImageFormSet, InquiryForm, ReplyForm, SearchForm


def home(request):
    featured_count = getattr(settings, 'FEATURED_PROPERTIES_COUNT', 5)
    featured = Property.objects.filter(status='active').order_by('-view_count')[:featured_count]
    search_form = SearchForm()
    return render(request, 'properties/home.html', {
        'featured_properties': featured,
        'search_form': search_form,
    })


def property_search(request):
    form = SearchForm(request.GET)
    properties = Property.objects.filter(status='active')

    # Read raw GET params (works whether or not SearchForm includes all fields)
    q            = request.GET.get('q', '').strip()
    listing_type = request.GET.get('listing_type', '').strip()
    property_type = request.GET.get('property_type', '').strip()

    # City / state search — searches city AND state so "Punjab" or "Ludhiana" both work
    if q:
        properties = properties.filter(
            Q(city__icontains=q) |
            Q(state__icontains=q) |
            Q(location__icontains=q) |
            Q(title__icontains=q)
        )

    if listing_type:
        properties = properties.filter(listing_type=listing_type)

    if property_type:
        properties = properties.filter(property_type=property_type)

    # Extra filters from SearchForm if valid
    if form.is_valid():
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        bedrooms  = form.cleaned_data.get('bedrooms')

        if min_price is not None:
            properties = properties.filter(price__gte=min_price)
        if max_price is not None:
            properties = properties.filter(price__lte=max_price)
        if bedrooms is not None:
            properties = properties.filter(bedrooms__gte=bedrooms)

    total = properties.count()
    return render(request, 'properties/property_list.html', {
        'properties': properties.order_by('-created_at'),
        'form': form,
        'total': total,
        'query': q,
    })


def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, status='active')
    property_obj.increment_view()

    inquiry_form = InquiryForm()

    if request.method == 'POST':
        inquiry_form = InquiryForm(request.POST)
        if inquiry_form.is_valid():
            inquiry = inquiry_form.save(commit=False)
            inquiry.property = property_obj
            if request.user.is_authenticated:
                inquiry.buyer = request.user
                inquiry.seeker_name = inquiry.seeker_name or request.user.full_name
            inquiry.save()

            _notify_seller_new_inquiry(inquiry, property_obj)

            messages.success(request, 'Your message has been sent to the owner!')
            return redirect('inquiry_thread', pk=inquiry.pk)

    return render(request, 'properties/property_detail.html', {
        'property': property_obj,
        'inquiry_form': inquiry_form,
        'images': property_obj.images.all(),
    })


def _notify_seller_new_inquiry(inquiry, property_obj):
    from django.core.mail import send_mail
    seller_email = property_obj.owner.email
    subject = f"New inquiry for your property: {property_obj.title}"
    message = f"""
Hello {property_obj.owner.full_name},

You have a new inquiry on your property "{property_obj.title}".

From: {inquiry.seeker_name}
Phone: {inquiry.seeker_phone or 'Not provided'}

Message:
{inquiry.message}

---
To reply, log in to your account and visit your inbox:
(Do NOT reply to this email — replies go through the platform to protect both parties)

Best regards,
{getattr(settings, 'SITE_NAME', 'HomeSathi')} Team
"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[seller_email],
            fail_silently=True,
        )
    except Exception:
        pass


@login_required
def inbox(request):
    seller_inquiries = Inquiry.objects.filter(
        property__owner=request.user
    ).select_related('property', 'buyer')

    buyer_inquiries = Inquiry.objects.filter(
        buyer=request.user
    ).select_related('property', 'property__owner')

    return render(request, 'properties/inbox.html', {
        'seller_inquiries': seller_inquiries,
        'buyer_inquiries': buyer_inquiries,
    })


@login_required
def inquiry_thread(request, pk):
    inquiry = get_object_or_404(Inquiry, pk=pk)
    user = request.user

    is_seller = (inquiry.property.owner == user)
    is_buyer  = (inquiry.buyer == user)

    if not (is_seller or is_buyer):
        return HttpResponseForbidden("You don't have access to this conversation.")

    if is_seller:
        inquiry.replies.filter(sender_role='buyer', is_read=False).update(is_read=True)
        if inquiry.status == 'pending':
            inquiry.status = 'read'
            inquiry.save(update_fields=['status'])
    elif is_buyer:
        inquiry.replies.filter(sender_role='seller', is_read=False).update(is_read=True)

    reply_form = ReplyForm()

    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            role = 'seller' if is_seller else 'buyer'
            InquiryReply.objects.create(
                inquiry=inquiry,
                sender=user,
                sender_role=role,
                message=reply_form.cleaned_data['message']
            )
            inquiry.status = 'replied'
            inquiry.save(update_fields=['status', 'updated_at'])

            _notify_reply(inquiry, role)

            messages.success(request, 'Reply sent!')
            return redirect('inquiry_thread', pk=pk)

    replies = inquiry.replies.all()

    return render(request, 'properties/inquiry_thread.html', {
        'inquiry': inquiry,
        'replies': replies,
        'reply_form': reply_form,
        'is_seller': is_seller,
        'is_buyer': is_buyer,
    })


def _notify_reply(inquiry, sender_role):
    from django.core.mail import send_mail

    if sender_role == 'seller':
        if inquiry.buyer:
            recipient_email = inquiry.buyer.email
            recipient_name  = inquiry.seeker_name
        else:
            return
        subject = f"The owner replied to your inquiry about: {inquiry.property.title}"
        body    = f"Hello {recipient_name},\n\nThe property owner has replied to your inquiry.\n\nLog in to read their reply and respond.\n\nDo NOT reply to this email — use the platform."
    else:
        recipient_email = inquiry.property.owner.email
        recipient_name  = inquiry.property.owner.full_name
        subject = f"New reply on your inquiry: {inquiry.property.title}"
        body    = f"Hello {recipient_name},\n\nThe buyer has replied to the inquiry on your property.\n\nLog in to read their reply.\n\nDo NOT reply to this email — use the platform."

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=True,
        )
    except Exception:
        pass


@login_required
def post_property_free(request):
    from .forms import PropertyForm
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner  = request.user
            property_obj.status = 'active'
            property_obj.save()

            images = request.FILES.getlist('property_images')
            for i, image in enumerate(images):
                from .models import PropertyImage
                PropertyImage.objects.create(
                    property=property_obj,
                    image=image,
                    is_primary=(i == 0)
                )

            messages.success(request, 'Your property has been listed successfully!')
            return redirect('my_properties')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = PropertyForm()

    return render(request, 'properties/post_propertyfree.html', {'form': form})


@login_required
def my_properties(request):
    properties = Property.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'properties/my_properties.html', {'properties': properties})


@login_required
def edit_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        form    = PropertyForm(request.POST, instance=property_obj)
        formset = PropertyImageFormSet(request.POST, request.FILES, instance=property_obj)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Property updated successfully!')
            return redirect('property_detail', pk=property_obj.pk)
    else:
        form    = PropertyForm(instance=property_obj)
        formset = PropertyImageFormSet(instance=property_obj)
    return render(request, 'properties/post_propertyfree.html', {
        'form': form, 'formset': formset, 'editing': True, 'property': property_obj,
    })


@login_required
def delete_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, 'Property deleted.')
<<<<<<< HEAD
    return redirect('my_properties')

from django.shortcuts import redirect, get_object_or_404

def mark_rented(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    prop.is_rented = True
    prop.save()
=======
>>>>>>> 37f5721e6e8a6a6e2687a9ac7f785021092f71e5
    return redirect('my_properties')