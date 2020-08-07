from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from blog.views import (
    must_authenticate_view
)

urlpatterns = [
    path('property/', include('property.urls')),
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('must_authenticate/', must_authenticate_view,
         name="must_authenticate"),

    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payments/', include('payments.urls')),
    # rest_framework
    path('api/property/', include('property.api.urls', 'property_api')),
    path('api/account/', include('blog.api.urls', 'blog_api'))
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
