from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('properties.urls')),
    path('users/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
<<<<<<< HEAD
  + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
=======
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
>>>>>>> 37f5721e6e8a6a6e2687a9ac7f785021092f71e5
