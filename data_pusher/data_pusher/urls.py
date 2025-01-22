from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('data_handler.urls')),  # Assuming all APIs are under the "api" route
]