
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/account/auth/', include('djoser.urls')),
    path('api/v1/account/auth/', include('djoser.urls.jwt')),
    re_path('', RedirectView.as_view(url='/')),
]
