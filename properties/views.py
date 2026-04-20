from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponseForbidden
import json

from .models import Property, Inquiry, InquiryReply
from .forms import PropertyForm, PropertyImageFormSet, InquiryForm, ReplyForm, SearchForm


def home(request):
    from django.db.models import Count, Avg
    active = Property.objects.filter(status='active')

    featured_properties  = active.order_by('-view_count')[:8]
    rent_props           = active.filter(listing_type='rent').order_by('-created_at')[:8]
    sale_props           = active.filter(listing_type='sell').order_by('-created_at')[:8]
    apartments           = active.filter(property_type='apartment').order_by('-created_at')[:8]
    villas               = active.filter(property_type='villa').order_by('-created_at')[:8]
    new_launches         = active.filter(listing_type='sell').order_by('-created_at')[:8]

    # BHK sections
    bhk1 = active.filter(bedrooms=1).order_by('-created_at')[:8]
    bhk2 = active.filter(bedrooms=2).order_by('-created_at')[:8]
    bhk3 = active.filter(bedrooms__gte=3).order_by('-created_at')[:8]

    # Budget segments (in rupees)
    affordable = active.filter(price__lte=5000000).order_by('price')[:8]        # up to 50L
    mid_segment = active.filter(price__gt=5000000, price__lte=15000000).order_by('price')[:8]  # 50L-1.5Cr
    luxury      = active.filter(price__gt=15000000).order_by('-price')[:8]      # 1.5Cr+

    # High demand = most viewed
    high_demand = active.order_by('-view_count')[:8]

    # Top gainer cities: cities with most listings
    top_cities_qs = (
        active.values('city')
        .annotate(count=Count('id'), avg_price=Avg('price'))
        .order_by('-count')[:6]
    )
    top_cities = [
        {
            'city': c['city'],
            'count': c['count'],
            'avg_price': int(c['avg_price'] or 0),
            'avg_price_display': (
                f"₹{c['avg_price']/10000000:.1f} Cr" if (c['avg_price'] or 0) >= 10000000
                else f"₹{c['avg_price']/100000:.1f} L" if (c['avg_price'] or 0) >= 100000
                else f"₹{int(c['avg_price'] or 0):,}"
            ),
            'bar_width': 0,  # filled below
        }
        for c in top_cities_qs
    ]
    max_count = max((c['count'] for c in top_cities), default=1)
    for c in top_cities:
        c['bar_width'] = int(c['count'] / max_count * 100)

    return render(request, 'properties/home.html', {
        'featured_properties': featured_properties,
        'rent_props':          rent_props,
        'sale_props':          sale_props,
        'apartments':          apartments,
        'villas':              villas,
        'new_launches':        new_launches,
        'bhk1':                bhk1,
        'bhk2':                bhk2,
        'bhk3':                bhk3,
        'affordable':          affordable,
        'mid_segment':         mid_segment,
        'luxury':              luxury,
        'bhk_map': [('bhk1', bhk1), ('bhk2', bhk2), ('bhk3', bhk3)],
        'high_demand':         high_demand,
        'top_cities':          top_cities,
    })


def property_search(request):
    form = SearchForm(request.GET)
    properties = Property.objects.filter(status='active')

    q             = request.GET.get('q', '').strip()
    listing_type  = request.GET.get('listing_type', '').strip()
    property_type = request.GET.get('property_type', '').strip()

    if q:
        properties = properties.filter(
            Q(city__icontains=q) | Q(state__icontains=q) |
            Q(location__icontains=q) | Q(title__icontains=q)
        )

    if listing_type:
        properties = properties.filter(listing_type=listing_type)
    if property_type:
        properties = properties.filter(property_type=property_type)

    if form.is_valid():
        d = form.cleaned_data
        if d.get('min_price') is not None:
            properties = properties.filter(price__gte=d['min_price'])
        if d.get('max_price') is not None:
            properties = properties.filter(price__lte=d['max_price'])
        if d.get('bedrooms') is not None:
            properties = properties.filter(bedrooms__gte=d['bedrooms'])
        if d.get('furnishing'):
            properties = properties.filter(furnishing=d['furnishing'])

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
                if not inquiry.seeker_name:
                    inquiry.seeker_name = request.user.full_name
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
    message = (
        f"Hello {property_obj.owner.full_name},\n\n"
        f"You have a new inquiry on \"{property_obj.title}\".\n\n"
        f"From: {inquiry.seeker_name}\n"
        f"Phone: {inquiry.seeker_phone or 'Not provided'}\n\n"
        f"Message:\n{inquiry.message}\n\n"
        f"---\nLog in to reply via the platform (do NOT reply to this email).\n\n"
        f"Best,\n{getattr(settings, 'SITE_NAME', 'HomeSathi')} Team"
    )
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [seller_email], fail_silently=True)
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
                inquiry=inquiry, sender=user,
                sender_role=role, message=reply_form.cleaned_data['message']
            )
            inquiry.status = 'replied'
            inquiry.save(update_fields=['status', 'updated_at'])
            _notify_reply(inquiry, role)
            messages.success(request, 'Reply sent!')
            return redirect('inquiry_thread', pk=pk)

    return render(request, 'properties/inquiry_thread.html', {
        'inquiry': inquiry,
        'replies': inquiry.replies.all(),
        'reply_form': reply_form,
        'is_seller': is_seller,
        'is_buyer': is_buyer,
    })


def _notify_reply(inquiry, sender_role):
    from django.core.mail import send_mail
    if sender_role == 'seller':
        if not inquiry.buyer:
            return
        recipient_email = inquiry.buyer.email
        recipient_name  = inquiry.seeker_name
        subject = f"Owner replied to your inquiry: {inquiry.property.title}"
        body    = f"Hello {recipient_name},\n\nThe owner replied. Log in to read and respond."
    else:
        recipient_email = inquiry.property.owner.email
        recipient_name  = inquiry.property.owner.full_name
        subject = f"New reply on: {inquiry.property.title}"
        body    = f"Hello {recipient_name},\n\nThe buyer replied. Log in to read."
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient_email], fail_silently=True)
    except Exception:
        pass


def _build_form_data_json(form):
    """
    Serialize form field values to a plain dict so the template can pass
    them to JavaScript via Django's json_script filter — no inline Django
    tags inside <script> blocks, no JS linter errors.
    """
    data = {}
    for field in form:
        val = field.value()
        if val is None:
            data[field.html_name] = ''
        else:
            data[field.html_name] = str(val)
    return json.dumps(data)


@login_required
def post_property_free(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner  = request.user
            property_obj.status = 'active'

            # Sync listing_type from the choice radio (named listing_type_choice in template)
            listing_type_choice = request.POST.get('listing_type_choice', '')
            if listing_type_choice:
                property_obj.listing_type = listing_type_choice

            # Sync furnishing from chip selection
            furnishing_status = request.POST.get('furnishing_status', '')
            if furnishing_status:
                property_obj.furnishing   = furnishing_status
                property_obj.is_furnished = (furnishing_status == 'furnished')

            # PG for field
            pg_for = request.POST.get('pg_for', '')
            if pg_for:
                property_obj.pg_for = pg_for

            property_obj.save()

            # Save images (multiple)
            images = request.FILES.getlist('property_images')
            for i, image in enumerate(images):
                from .models import PropertyImage
                PropertyImage.objects.create(
                    property=property_obj,
                    image=image,
                    is_primary=(i == 0),
                    order=i,
                )

            messages.success(request, 'Your property has been listed successfully!')
            return redirect('property_detail', pk=property_obj.pk)
        else:
            # Form invalid — re-render with errors.
            # Build form_data_json so JS can restore field values after reload.
            messages.error(request, 'Please fix the errors below.')
            return render(request, 'properties/post_propertyfree.html', {
                'form': form,
                'form_data_json': _build_form_data_json(form),
            })
    else:
        form = PropertyForm()

    return render(request, 'properties/post_propertyfree.html', {
        'form': form,
        'form_data_json': '{}',   # empty on fresh GET — JS restoreOnError will be a no-op
    })


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
            messages.success(request, 'Property updated!')
            return redirect('property_detail', pk=property_obj.pk)
        else:
            return render(request, 'properties/post_propertyfree.html', {
                'form': form,
                'formset': formset,
                'editing': True,
                'property': property_obj,
                'form_data_json': _build_form_data_json(form),
            })
    else:
        form    = PropertyForm(instance=property_obj)
        formset = PropertyImageFormSet(instance=property_obj)

    return render(request, 'properties/post_propertyfree.html', {
        'form': form,
        'formset': formset,
        'editing': True,
        'property': property_obj,
        'form_data_json': _build_form_data_json(form),
    })


@login_required
def delete_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, 'Property deleted.')
    return redirect('my_properties')


def mark_rented(request, pk):
    prop = get_object_or_404(Property, pk=pk, owner=request.user)
    prop.is_rented = True
    prop.status = 'sold'
    prop.save()
    return redirect('my_properties')


# ── REVIEWS ────────────────────────────────────────────────────────────────
from django.db.models import Avg, Count
from .models import Review


def _build_bar_and_stars(star_counts, max_count, avg):
    labels = {5: 'FIVE', 4: 'FOUR', 3: 'THREE', 2: 'TWO', 1: 'ONE'}
    bar_data = []
    for star in [5, 4, 3, 2, 1]:
        count = star_counts[star]
        width = int(round(count / max_count * 100)) if max_count else 0
        bar_data.append({'star': star, 'label': labels[star], 'count': count, 'width': width})
    avg_rounded = round(avg)
    avg_stars = [i <= avg_rounded for i in range(1, 6)]
    return bar_data, avg_stars


def reviews_page(request):
    approved    = Review.objects.filter(is_approved=True)
    stats       = approved.values('rating').annotate(count=Count('rating')).order_by('rating')
    total       = approved.count()
    avg         = approved.aggregate(avg=Avg('rating'))['avg'] or 0
    star_counts = {i: 0 for i in range(1, 6)}
    for s in stats:
        star_counts[s['rating']] = s['count']
    max_count = max(star_counts.values()) if total else 1

    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        rating  = request.POST.get('rating', '').strip()
        message = request.POST.get('message', '').strip()
        error = None
        if not name or not email or not rating or not message:
            error = "All fields are required."
        elif not rating.isdigit() or not (1 <= int(rating) <= 5):
            error = "Please select a valid star rating (1–5)."
        if error:
            bar_data, avg_stars = _build_bar_and_stars(star_counts, max_count, avg)
            return render(request, 'properties/reviews.html', {
                'approved_reviews': approved, 'total': total,
                'avg_display': round(avg, 1) if avg else 0,
                'bar_data': bar_data, 'avg_stars': avg_stars,
                'error': error, 'success': False,
            })
        Review.objects.create(name=name, email=email, rating=int(rating), message=message, is_approved=False)
        return redirect(request.path + '?submitted=1')

    success = request.GET.get('submitted') == '1'
    bar_data, avg_stars = _build_bar_and_stars(star_counts, max_count, avg)
    return render(request, 'properties/reviews.html', {
        'approved_reviews': approved, 'total': total,
        'avg_display': round(avg, 1) if avg else 0,
        'bar_data': bar_data, 'avg_stars': avg_stars,
        'error': None, 'success': success,
    })
def budget(request):
    return render(request, 'properties/budget.html')