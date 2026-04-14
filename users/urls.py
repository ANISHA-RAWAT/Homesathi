from django.urls import path
from . import views

urlpatterns = [

    # ───────── AUTH ─────────
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ───────── EMAIL VERIFICATION ─────────
    path('confirm-signup/<uuid:token>/', views.confirm_signup, name='confirm_signup'),
    path('verification-sent/', views.verification_sent, name='verification_sent'),

    # ───────── USER ─────────
    path('profile/', views.profile_view, name='profile'),
    path('faq/', views.faq, name='faq'),
    path('contactus/', views.contactus, name='contactus'),
    path('contact-send/', views.contact_view, name='contact_view'),
    path('about/', views.about, name='about'),
    path('review/', views.review, name='review'),

]