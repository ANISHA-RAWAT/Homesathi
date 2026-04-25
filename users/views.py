from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

from .forms import SignupForm, LoginForm
from .models import PendingUser

User = get_user_model()


# ─────────────────────────────────────────────────────────────
# SIGNUP
# ─────────────────────────────────────────────────────────────
def signup_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            if User.objects.filter(email=email).exists():
                messages.error(request, "Account already exists. Please login.")
                return redirect('login')

            PendingUser.objects.filter(email=email).delete()

            pending = PendingUser.objects.create(
                email=email,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone=form.cleaned_data.get('phone', ''),
                password=make_password(form.cleaned_data['password1'])
            )

            verify_url = request.build_absolute_uri(
                reverse('confirm_signup', args=[str(pending.token)])
            )

            # Absolute URL for logo so it loads in email clients
            logo_url = request.build_absolute_uri(settings.STATIC_URL + 'images/logo1.png')

            # ── Plain text fallback ──
            plain_text = f"""Hi {pending.first_name},

Thank you for signing up with HomeSathi!

Click the link below to verify your account:

{verify_url}

This link expires in 24 hours.

If you did not create this account, please ignore this email.

— HomeSathi Team
"""

            # ── HTML email with logo ──
            html_message = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background:#f4f6f9;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f6f9;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="100%" cellpadding="0" cellspacing="0"
               style="max-width:560px;background:#ffffff;border-radius:16px;
                      box-shadow:0 4px 24px rgba(0,0,0,0.08);overflow:hidden;">

          <!-- HEADER -->
          <tr>
            <td align="center"
                style="background:linear-gradient(135deg,#00A9FF,#0090d9);padding:36px 40px 28px;">
              <img src="{logo_url}" alt="HomeSathi" width="80" height="80"
                   style="border-radius:50%;border:3px solid rgba(255,255,255,0.4);
                          display:block;margin:0 auto 14px;">
              <h1 style="margin:0;color:#ffffff;font-size:1.5rem;font-weight:700;">HomeSathi</h1>
              <p style="margin:4px 0 0;color:rgba(255,255,255,0.85);font-size:0.9rem;">
                Find your perfect space
              </p>
            </td>
          </tr>

          <!-- BODY -->
          <tr>
            <td style="padding:36px 40px 28px;">
              <p style="margin:0 0 8px;font-size:1.05rem;color:#1a1a1a;font-weight:600;">
                Hi {pending.first_name},
              </p>
              <p style="margin:0 0 24px;color:#555;line-height:1.7;">
                Thank you for creating your HomeSathi account!
                Please verify your email address to get started.
              </p>

              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td align="center" style="padding:4px 0 28px;">
                    <a href="{verify_url}"
                       style="display:inline-block;background:linear-gradient(135deg,#00A9FF,#0090d9);
                              color:#ffffff;text-decoration:none;font-weight:700;font-size:1rem;
                              padding:14px 40px;border-radius:10px;
                              box-shadow:0 4px 14px rgba(0,169,255,0.35);">
                      Verify My Account
                    </a>
                  </td>
                </tr>
              </table>

              <p style="margin:0 0 6px;font-size:0.82rem;color:#999;">
                Button not working? Copy and paste this link into your browser:
              </p>
              <p style="margin:0 0 24px;word-break:break-all;">
                <a href="{verify_url}" style="color:#00A9FF;font-size:0.82rem;text-decoration:none;">
                  {verify_url}
                </a>
              </p>

              <div style="background:#fffbeb;border:1px solid #fde68a;
                          border-radius:10px;padding:14px 18px;">
                <p style="margin:0;font-size:0.88rem;color:#92400e;line-height:1.6;">
                  <strong>This link expires in 24 hours.</strong>
                  If you didn't create a HomeSathi account, you can safely ignore this email.
                </p>
              </div>
            </td>
          </tr>

          <!-- FOOTER -->
          <tr>
            <td align="center"
                style="background:#f8fafc;border-top:1px solid #e5e7eb;padding:20px 40px;">
              <p style="margin:0;font-size:0.8rem;color:#9ca3af;">
                &copy; 2026 HomeSathi. All rights reserved.<br>
                Owner contact details are never publicly revealed.
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

            try:
                email_msg = EmailMultiAlternatives(
                    subject='Verify your HomeSathi account',
                    body=plain_text,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[pending.email],
                )
                email_msg.attach_alternative(html_message, "text/html")
                email_msg.send(fail_silently=False)

            except Exception:
                pending.delete()
                form.add_error(None, "Could not send verification email. Please check your email address and try again.")
                return render(request, 'users/signup.html', {'form': form})

            messages.success(request, "Verification email sent. Please check your inbox.")
            return redirect('verification_sent')

    else:
        form = SignupForm()

    return render(request, 'users/signup.html', {'form': form})


# ─────────────────────────────────────────────────────────────
# CONFIRM SIGNUP
# ─────────────────────────────────────────────────────────────
def confirm_signup(request, token):

    try:
        pending = PendingUser.objects.get(token=token)
    except PendingUser.DoesNotExist:
        messages.error(request, "Invalid or expired verification link.")
        return redirect('signup')

    if pending.is_expired():
        pending.delete()
        messages.error(request, "Verification link expired. Please signup again.")
        return redirect('signup')

    user = User.objects.create(
        email=pending.email,
        username=pending.email,
        first_name=pending.first_name,
        last_name=pending.last_name,
        phone=pending.phone,
        password=pending.password,
        is_active=True,
    )

    pending.delete()

    messages.success(request, "Account verified successfully! Please login.")
    return redirect('login')


# ─────────────────────────────────────────────────────────────
# VERIFICATION SENT PAGE
# ─────────────────────────────────────────────────────────────
def verification_sent(request):
    return render(request, 'users/resend_verification.html')


# ─────────────────────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────────────────────
def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.full_name}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")

    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


# ─────────────────────────────────────────────────────────────
# LOGOUT
# ─────────────────────────────────────────────────────────────
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


# ─────────────────────────────────────────────────────────────
# PROFILE
# ─────────────────────────────────────────────────────────────
@login_required
def profile_view(request):
    return render(request, 'users/profile.html')


# ─────────────────────────────────────────────────────────────
# STATIC PAGES
# ─────────────────────────────────────────────────────────────
def faq(request):
    return render(request, 'properties/faq.html')

def about(request):
    return render(request, 'properties/about.html')


# ─────────────────────────────────────────────────────────────
# CONTACT US
# ─────────────────────────────────────────────────────────────
def contactus(request):
    return render(request, 'properties/contactus.html')

def contact_view(request):
    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not message:
            messages.error(request, "Please fill in all fields.")
            return render(request, 'properties/contactus.html')

        try:
            send_mail(
                subject=f"New Contact Message from {name}",
                message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            messages.success(request, "Message sent successfully! We'll get back to you soon.")
        except Exception:
            messages.error(request, "Failed to send message. Please email us directly.")

        return redirect('contactus')

    return render(request, 'properties/contactus.html')


# ─────────────────────────────────────────────────────────────
# REVIEWS
# ─────────────────────────────────────────────────────────────
def review(request):
    from properties.models import Review
    from django.db.models import Avg, Count

    if request.method == 'POST':
        name         = request.POST.get('name', '').strip()
        email        = request.POST.get('email', '').strip()
        rating       = request.POST.get('rating', '').strip()
        message_text = request.POST.get('message', '').strip()

        if not name or not email or not message_text:
            messages.error(request, "Please fill in all fields.")
        elif not rating:
            messages.error(request, "Please select a star rating before submitting.")
        elif not rating.isdigit() or not (1 <= int(rating) <= 5):
            messages.error(request, "Please select a valid star rating (1–5).")
        else:
            Review.objects.create(
                name=name, email=email,
                rating=int(rating), message=message_text,
                is_approved=False,
            )
            messages.success(request,
                "Your review has been submitted! It will appear here once approved by our team.")
            return redirect('review')

    approved    = Review.objects.filter(is_approved=True)
    stats       = approved.values('rating').annotate(count=Count('rating')).order_by('rating')
    total       = approved.count()
    avg         = approved.aggregate(avg=Avg('rating'))['avg'] or 0
    star_counts = {i: 0 for i in range(1, 6)}
    for s in stats:
        star_counts[s['rating']] = s['count']
    max_count = max(star_counts.values()) if total else 1
    labels    = {5: 'FIVE', 4: 'FOUR', 3: 'THREE', 2: 'TWO', 1: 'ONE'}
    bar_data  = [
        {'star': star, 'label': labels[star],
         'count': star_counts[star],
         'width': int(round(star_counts[star] / max_count * 100)) if max_count else 0}
        for star in [5, 4, 3, 2, 1]
    ]
    avg_stars = [i <= round(avg) for i in range(1, 6)]

    return render(request, 'properties/review.html', {
        'approved_reviews': approved,
        'total':       total,
        'avg_display': round(avg, 1) if avg else 0,
        'bar_data':    bar_data,
        'avg_stars':   avg_stars,
    })