from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.db.models import Q, Avg, Count
from django.http import HttpResponseForbidden
import json
import logging

from .models import Property, Inquiry, InquiryReply, Review
from .forms import PropertyForm, PropertyImageFormSet, InquiryForm, ReplyForm, SearchForm

logger = logging.getLogger(__name__)


# ── HOME ──────────────────────────────────────────────────────────────────────
def home(request):
    active = Property.objects.filter(status='active')

    featured_properties = active.order_by('-view_count')[:8]
    rent_props          = active.filter(listing_type='rent').order_by('-created_at')[:8]
    sale_props          = active.filter(listing_type='sell').order_by('-created_at')[:8]
    apartments          = active.filter(property_type='flat_apartment').order_by('-created_at')[:8]
    villas              = active.filter(property_type='independent_house_villa').order_by('-created_at')[:8]
    new_launches        = active.order_by('-created_at')[:20]

    bhk1 = active.filter(bedrooms=1).order_by('-created_at')[:8]
    bhk2 = active.filter(bedrooms=2).order_by('-created_at')[:8]
    bhk3 = active.filter(bedrooms__gte=3).order_by('-created_at')[:8]

    affordable  = active.filter(price__lte=5000000).order_by('price')[:8]
    mid_segment = active.filter(price__gt=5000000, price__lte=15000000).order_by('price')[:8]
    luxury      = active.filter(price__gt=15000000).order_by('-price')[:8]
    high_demand = active.order_by('-view_count')[:8]

    top_cities_qs = (
        active.values('city')
        .annotate(count=Count('id'), avg_price=Avg('price'))
        .order_by('-count')[:10]
    )
    top_cities = []
    for c in top_cities_qs:
        avg = c['avg_price'] or 0
        top_cities.append({
            'city': c['city'],
            'count': c['count'],
            'avg_price': int(avg),
            'avg_price_display': (
                f"₹{avg/10000000:.1f} Cr" if avg >= 10000000
                else f"₹{avg/100000:.1f} L" if avg >= 100000
                else f"₹{int(avg):,}"
            ),
            'bar_width': 0,
        })
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


# ── SEARCH ────────────────────────────────────────────────────────────────────
def property_search(request):
    form       = SearchForm(request.GET)
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
        'form':       form,
        'total':      total,
        'query':      q,
    })


# ── DETAIL ────────────────────────────────────────────────────────────────────
def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, status='active')
    property_obj.increment_view()

    reviews = Review.objects.filter(
        related_property=property_obj, is_approved=True
    ).select_related('reviewer')

    stats            = reviews.aggregate(avg_p=Avg('property_rating'), avg_o=Avg('owner_rating'), total=Count('id'))
    total_reviews    = stats['total'] or 0
    avg_prop_rating  = round(stats['avg_p'] or 0, 1)
    avg_owner_rating = round(stats['avg_o'] or 0, 1)
    avg_overall      = round((avg_prop_rating + avg_owner_rating) / 2, 1) if total_reviews else 0

    property_star_counts = {i: 0 for i in range(1, 6)}
    for r in reviews:
        property_star_counts[r.property_rating] = property_star_counts.get(r.property_rating, 0) + 1

    user_has_reviewed = False
    user_review       = None
    if request.user.is_authenticated:
        user_review       = Review.objects.filter(related_property=property_obj, reviewer=request.user).first()
        user_has_reviewed = user_review is not None

    inquiry_form = InquiryForm()

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'submit_review':
            if not request.user.is_authenticated:
                messages.error(request, 'Please log in to leave a review.')
            elif request.user == property_obj.owner:
                messages.error(request, 'You cannot review your own property.')
            elif user_has_reviewed:
                messages.error(request, 'You have already reviewed this property.')
            else:
                prop_rating  = request.POST.get('property_rating', '').strip()
                owner_rating = request.POST.get('owner_rating', '').strip()
                comment      = request.POST.get('comment', '').strip()
                if not prop_rating or not owner_rating or not comment:
                    messages.error(request, 'All review fields are required.')
                elif not (prop_rating.isdigit() and owner_rating.isdigit()
                          and 1 <= int(prop_rating) <= 5 and 1 <= int(owner_rating) <= 5):
                    messages.error(request, 'Ratings must be between 1 and 5.')
                else:
                    Review.objects.update_or_create(
                        related_property=property_obj,
                        reviewer=request.user,
                        defaults=dict(
                            property_rating=int(prop_rating),
                            owner_rating=int(owner_rating),
                            comment=comment,
                            is_approved=True,
                        ),
                    )
                    messages.success(request, 'Your review has been posted!')
                    return redirect('property_detail', pk=pk)

        elif action == 'edit_review':
            if request.user.is_authenticated and user_review:
                prop_rating  = request.POST.get('property_rating', '').strip()
                owner_rating = request.POST.get('owner_rating', '').strip()
                comment      = request.POST.get('comment', '').strip()
                if prop_rating and owner_rating and comment:
                    user_review.property_rating = int(prop_rating)
                    user_review.owner_rating    = int(owner_rating)
                    user_review.comment         = comment
                    user_review.save()
                    messages.success(request, 'Your review has been updated!')
                    return redirect('property_detail', pk=pk)

        else:
            inquiry_form = InquiryForm(request.POST)
            if inquiry_form.is_valid():
                if request.user.is_authenticated and request.user == property_obj.owner:
                    messages.error(request, 'You cannot send an inquiry to your own property.')
                    return redirect('property_detail', pk=pk)
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
        'property':             property_obj,
        'inquiry_form':         inquiry_form,
        'images':               property_obj.images.all(),
        'reviews':              reviews,
        'total_reviews':        total_reviews,
        'avg_prop_rating':      avg_prop_rating,
        'avg_owner_rating':     avg_owner_rating,
        'avg_overall':          avg_overall,
        'property_star_counts': property_star_counts,
        'user_has_reviewed':    user_has_reviewed,
        'user_review':          user_review,
        'review_form':          {},
    })


@login_required
def delete_review(request, pk, review_pk):
    property_obj = get_object_or_404(Property, pk=pk)
    review = get_object_or_404(Review, pk=review_pk, related_property=property_obj, reviewer=request.user)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Your review has been deleted.')
    return redirect('property_detail', pk=pk)


# ── POST PROPERTY FREE ────────────────────────────────────────────────────────
@login_required
def post_property_free(request):
    if request.method == 'POST':
        post_data = request.POST.copy()

        # ── 1. Map hidden JS fields → Django field names ──────────────────
        listing_type_choice = post_data.get('listing_type_choice', '').strip()
        if listing_type_choice:
            post_data['listing_type'] = listing_type_choice

        if not post_data.get('property_type', '').strip():
            ht = post_data.get('hPropertyType', '').strip()
            if ht:
                post_data['property_type'] = ht

        if not post_data.get('property_category', '').strip():
            hc = post_data.get('hCategory', '').strip()
            if hc:
                post_data['property_category'] = hc

        if not post_data.get('seller_type', '').strip():
            hs = post_data.get('hSellerType', '').strip()
            if hs:
                post_data['seller_type'] = hs

        # ── 2. PG: force correct type + listing ──────────────────────────
        if post_data.get('seller_type') == 'pg_owner' or post_data.get('property_category') == 'pg':
            post_data['listing_type']  = 'pg'
            post_data['property_type'] = 'pg_hostel'

        # ── 3. furnishing_status → furnishing ────────────────────────────
        furnishing_status = post_data.get('furnishing_status', '').strip()
        if furnishing_status:
            post_data['furnishing'] = furnishing_status

        # ── 4. PG: map pg_amenities → pg_common_areas ────────────────────
        # pp-form-pg.js sends amenities as 'pg_amenities' and 'common_areas'
        # We merge them all into pg_common_areas for the model
        pg_amenities  = post_data.getlist('pg_amenities')
        common_areas  = post_data.getlist('common_areas')
        room_furnishing = post_data.getlist('room_furnishing')

        if pg_amenities or common_areas:
            # Combine into pg_common_areas, deduplicated
            combined = list(set(pg_amenities + common_areas))
            post_data.setlist('pg_common_areas', combined)

        # ── 5. Plot-specific multi-fields → store in amenities ────────────
        # Owner/builder plot forms send 'plot_amenities', 'utilities', 'legal_status'
        # We store them all together in amenities JSON field
        plot_amenities = post_data.getlist('plot_amenities')
        utilities      = post_data.getlist('utilities')
        legal_status   = post_data.getlist('legal_status')

        if plot_amenities or utilities or legal_status:
            existing_amenities = post_data.getlist('amenities')
            merged = list(set(existing_amenities + plot_amenities + utilities + legal_status))
            post_data.setlist('amenities', merged)

        # ── 6. room_furnishing → furnishing_items (PG room items) ─────────
        if room_furnishing:
            existing_furnishing = post_data.getlist('furnishing_items')
            merged_furn = list(set(existing_furnishing + room_furnishing))
            post_data.setlist('furnishing_items', merged_furn)

        form = PropertyForm(post_data, request.FILES)

        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner  = request.user
            property_obj.status = 'active'

            # Furnishing sync
            if furnishing_status:
                property_obj.furnishing   = furnishing_status
                property_obj.is_furnished = (furnishing_status == 'furnished')

            # pg_for from chip radio
            pg_for = post_data.get('pg_for', '').strip()
            if pg_for:
                property_obj.pg_for = pg_for

            # bathroom_type — stored in a custom field not on the model directly
            # so we store it as part of key_facilities or ignore (model has no field)
            # If you add bathroom_type to the model later, uncomment:
            # property_obj.bathroom_type = post_data.get('bathroom_type', '')

            # Plot-specific extra fields (not on the model — store as text in key_facilities)
            _patch_plot_fields(property_obj, post_data)

            # Null guards
            if property_obj.bedrooms is None:
                property_obj.bedrooms = 0
            if property_obj.bathrooms is None:
                property_obj.bathrooms = 0

            property_obj.save()

            # Save JSON multi-fields
            for json_field in ('amenities', 'furnishing_items', 'overlooking', 'pg_common_areas'):
                val = form.cleaned_data.get(json_field, [])
                setattr(property_obj, json_field, list(val))
            property_obj.save(update_fields=['amenities', 'furnishing_items', 'overlooking', 'pg_common_areas'])

            # Save images
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
            # Log full errors for debugging, show simplified message to user
            logger.error("Property form errors for user %s: %s", request.user, form.errors.as_json())
            messages.error(request, f'Please fix the errors below: {dict(form.errors)}')
            return render(request, 'properties/post_propertyfree.html', {
                'form':           form,
                'form_data_json': _build_form_data_json(form),
            })

    else:
        form = PropertyForm()

    return render(request, 'properties/post_propertyfree.html', {
        'form':           form,
        'form_data_json': '{}',
    })


def _patch_plot_fields(property_obj, post_data):
    """
    Store plot-specific fields that have no dedicated model column.
    We serialise them into key_highlights so nothing is silently dropped.
    """
    extras = {}

    plot_type = post_data.get('plot_type', '').strip()
    if plot_type:
        extras['Plot Type'] = plot_type

    plot_length = post_data.get('plot_length', '').strip()
    plot_width  = post_data.get('plot_width', '').strip()
    if plot_length or plot_width:
        extras['Dimensions'] = f"{plot_length} × {plot_width}"

    plot_area = post_data.get('plot_area', '').strip()
    if plot_area:
        area_unit = post_data.get('area_unit', 'sqft')
        extras['Plot Area'] = f"{plot_area} {area_unit}"

    open_sides = post_data.get('open_sides', '').strip()
    if open_sides:
        extras['Open Sides'] = open_sides

    approved_for_construction = post_data.get('approved_for_construction', '').strip()
    if approved_for_construction:
        extras['Approved for Construction'] = approved_for_construction

    boundary_wall = post_data.get('boundary_wall', '').strip()
    if boundary_wall:
        extras['Boundary Wall'] = boundary_wall

    if extras:
        existing = property_obj.key_highlights or ''
        addition = ' | '.join(f"{k}: {v}" for k, v in extras.items())
        property_obj.key_highlights = f"{existing}\n{addition}".strip() if existing else addition


# ── MY PROPERTIES ─────────────────────────────────────────────────────────────
@login_required
def my_properties(request):
    properties = Property.objects.filter(owner=request.user).order_by('-created_at').prefetch_related('inquiries')
    return render(request, 'properties/my_properties.html', {'properties': properties})


# ── EDIT PROPERTY ─────────────────────────────────────────────────────────────
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
            logger.error("Edit form errors for property %s: %s", pk, form.errors.as_json())
            return render(request, 'properties/post_propertyfree.html', {
                'form':           form,
                'formset':        formset,
                'editing':        True,
                'property':       property_obj,
                'form_data_json': _build_form_data_json(form),
            })
    else:
        form    = PropertyForm(instance=property_obj)
        formset = PropertyImageFormSet(instance=property_obj)

    return render(request, 'properties/post_propertyfree.html', {
        'form':           form,
        'formset':        formset,
        'editing':        True,
        'property':       property_obj,
        'form_data_json': _build_form_data_json(form),
    })


# ── DELETE PROPERTY ───────────────────────────────────────────────────────────
@login_required
def delete_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, 'Property deleted.')
    return redirect('my_properties')


# ── MARK RENTED ───────────────────────────────────────────────────────────────
@login_required
def mark_rented(request, pk):
    prop = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        rented_to_pk = request.POST.get('rented_to_inquiry_pk') or None
        prop.is_rented = True
        prop.status    = 'sold'
        prop.save(update_fields=['is_rented', 'status'])

        exclude_pk = None
        if rented_to_pk:
            try:
                chosen     = Inquiry.objects.get(pk=rented_to_pk, property=prop)
                exclude_pk = chosen.pk
            except Inquiry.DoesNotExist:
                pass

        _notify_rented_to_others(prop, exclude_inquiry_pk=exclude_pk)
        messages.success(request, 'Property marked as rented. Other inquirers have been notified automatically.')
    return redirect('my_properties')


# ── REPOST PROPERTY ───────────────────────────────────────────────────────────
@login_required
def repost_property(request, pk):
    prop = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        prop.is_rented = False
        prop.status    = 'active'
        prop.save(update_fields=['is_rented', 'status'])
        messages.success(request, f'"{prop.title}" is now live again!')
    return redirect('my_properties')


# ── INBOX ──────────────────────────────────────────────────────────────────────
@login_required
def inbox(request):
    from collections import defaultdict
    seller_inquiries = Inquiry.objects.filter(
        property__owner=request.user
    ).select_related('property', 'buyer').order_by('property__id', '-updated_at')

    properties_with_inquiries = defaultdict(list)
    for inq in seller_inquiries:
        properties_with_inquiries[inq.property].append(inq)

    buyer_inquiries = Inquiry.objects.filter(
        buyer=request.user
    ).exclude(
        property__owner=request.user
    ).select_related('property', 'property__owner').order_by('-updated_at')

    buyer_inquiries_list = list(buyer_inquiries)
    return render(request, 'properties/inbox.html', {
        'properties_with_inquiries': dict(properties_with_inquiries),
        'buyer_inquiries':           buyer_inquiries_list,
        'seller_count':              len(properties_with_inquiries),
        'buyer_count':               len(buyer_inquiries_list),
    })


# ── INQUIRY THREAD ────────────────────────────────────────────────────────────
@login_required
def inquiry_thread(request, pk):
    inquiry   = get_object_or_404(Inquiry, pk=pk)
    user      = request.user
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
        'inquiry':    inquiry,
        'replies':    inquiry.replies.all(),
        'reply_form': reply_form,
        'is_seller':  is_seller,
        'is_buyer':   is_buyer,
    })


# ── REVIEWS PAGE ──────────────────────────────────────────────────────────────
def reviews_page(request):
    approved    = Review.objects.filter(is_approved=True, related_property__isnull=True)
    stats       = approved.values('property_rating').annotate(count=Count('property_rating')).order_by('property_rating')
    total       = approved.count()
    avg         = approved.aggregate(avg=Avg('property_rating'))['avg'] or 0
    star_counts = {i: 0 for i in range(1, 6)}
    for s in stats:
        star_counts[s['property_rating']] = s['count']
    max_count = max(star_counts.values()) if total else 1

    user_already_reviewed = (
        request.user.is_authenticated and
        Review.objects.filter(reviewer=request.user, related_property__isnull=True).exists()
    )

    error   = None
    success = request.GET.get('submitted') == '1'

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to leave a review.')
            return redirect('login')

        if user_already_reviewed:
            error = "You have already submitted a site-wide review. Thank you!"
        else:
            rating  = request.POST.get('rating', '').strip()
            comment = request.POST.get('comment', '').strip()
            if not rating or not comment:
                error = "Both a star rating and a comment are required."
            elif not rating.isdigit() or not (1 <= int(rating) <= 5):
                error = "Please select a valid star rating (1–5)."
            else:
                Review.objects.create(
                    reviewer=request.user,
                    related_property=None,
                    property_rating=int(rating),
                    owner_rating=int(rating),
                    comment=comment,
                    is_approved=False,
                )
                return redirect(request.path + '?submitted=1')

    bar_data, avg_stars = _build_bar_and_stars(star_counts, max_count, avg)
    return render(request, 'properties/reviews.html', {
        'approved_reviews':      approved,
        'total':                 total,
        'avg_display':           round(avg, 1) if avg else 0,
        'bar_data':              bar_data,
        'avg_stars':             avg_stars,
        'error':                 error,
        'success':               success,
        'user_already_reviewed': user_already_reviewed,
    })


# ── BUDGET CALCULATOR ─────────────────────────────────────────────────────────
def budget_calculator(request):
    return render(request, 'properties/budget_calculator.html')


# ═════════════════════════════════════════════════════════════════════════════
#  PRIVATE HELPERS
# ═════════════════════════════════════════════════════════════════════════════

def _build_form_data_json(form):
    data = {}
    for field in form:
        val = field.value()
        data[field.html_name] = '' if val is None else str(val)
    return json.dumps(data)


def _build_bar_and_stars(star_counts, max_count, avg):
    labels   = {5: 'FIVE', 4: 'FOUR', 3: 'THREE', 2: 'TWO', 1: 'ONE'}
    bar_data = []
    for star in [5, 4, 3, 2, 1]:
        count = star_counts[star]
        width = int(round(count / max_count * 100)) if max_count else 0
        bar_data.append({'star': star, 'label': labels[star], 'count': count, 'width': width})
    avg_rounded = round(avg)
    avg_stars   = [i <= avg_rounded for i in range(1, 6)]
    return bar_data, avg_stars


def _notify_seller_new_inquiry(inquiry, property_obj):
    from django.core.mail import send_mail
    seller_email = property_obj.owner.email
    subject      = f"New inquiry for your property: {property_obj.title}"
    message      = (
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
        from django.core.mail import send_mail
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient_email], fail_silently=True)
    except Exception:
        pass


def _notify_rented_to_others(prop, exclude_inquiry_pk=None):
    from django.core.mail import send_mail
    qs = Inquiry.objects.filter(property=prop)
    if exclude_inquiry_pk:
        qs = qs.exclude(pk=exclude_inquiry_pk)

    for inquiry in qs:
        InquiryReply.objects.create(
            inquiry=inquiry,
            sender=None,
            sender_role='seller',
            message=(
                f"🏠 Update: This property has been rented/sold. "
                f"Thank you for your interest in \"{prop.title}\". "
                f"We hope you find the perfect place soon — "
                f"please explore our other available listings!"
            ),
        )
        inquiry.status = 'closed'
        inquiry.save(update_fields=['status', 'updated_at'])

        if inquiry.buyer and inquiry.buyer.email:
            try:
                send_mail(
                    subject=f"Property no longer available: {prop.title}",
                    message=(
                        f"Hello {inquiry.seeker_name},\n\n"
                        f"We wanted to let you know that \"{prop.title}\" "
                        f"in {prop.city} has been rented/sold and is no longer available.\n\n"
                        f"Please visit our platform to explore other listings.\n\n"
                        f"Best regards,\n"
                        f"{getattr(settings, 'SITE_NAME', 'HomeSathi')} Team"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[inquiry.buyer.email],
                    fail_silently=True,
                )
            except Exception:
                pass