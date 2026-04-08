from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

from .forms import SignupForm, LoginForm
from .models import PendingUser

User = get_user_model()


# ─────────────────────────────────────────────────────────────
# SIGNUP (User NOT saved yet)
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

            send_mail(
                subject='Confirm Your Signup — Rental Platform',
                message=f"""
Hi {pending.first_name},

Thank you for signing up!

Click the link below to verify your account:

{verify_url}

⚠️ This link expires in 24 hours.

If you did not create this account, ignore this email.

— Rental Platform Team
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[pending.email],
                fail_silently=False,
            )

            messages.success(request, "Verification email sent. Please check your inbox.")
            return redirect('verification_sent')

    else:
        form = SignupForm()

    return render(request, 'users/signup.html', {'form': form})


# ─────────────────────────────────────────────────────────────
# CONFIRM SIGNUP — only ONE definition, with is_active=True
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
    return render(request, 'verification_sent.html')


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
def faq(request):
    return render(request, 'properties/faq.html')
