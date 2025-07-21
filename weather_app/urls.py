from django.urls import path
from .import views
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('weather_app.urls')),
]