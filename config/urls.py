
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/account/auth/', include('djoser.urls')),
    path('api/v1/account/auth/', include('djoser.urls.jwt')),
    path('api/v1/', include('apiv1.urls')),
]
