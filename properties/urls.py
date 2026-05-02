from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.property_search, name='property_search'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),

    path('post-property-free/', views.post_property_free, name='post_propertyfree'),

    path('property/<int:pk>/edit/', views.edit_property, name='edit_property'),
    path('property/<int:pk>/delete/', views.delete_property, name='delete_property'),
    path('my-properties/', views.my_properties, name='my_properties'),
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/<int:pk>/', views.inquiry_thread, name='inquiry_thread'),
    path('mark-rented/<int:pk>/', views.mark_rented, name='mark_rented'),
    path('repost-property/<int:pk>/', views.repost_property, name='repost_property'),
    path('reviews/', views.reviews_page, name='reviews'),
    path('budget_calculator/', views.budget_calculator, name='budget_calculator'),

    # ── Property Reviews ──
    path('property/<int:pk>/review/delete/<int:review_pk>/', views.delete_review, name='delete_review'),
]