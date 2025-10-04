from django.urls import path, include
from .views import me, register

urlpatterns = [
  path('api/me', me, name='api_me'),
  path('api/register', register, name='api_register'),
  path('api/', include('core.urls')),
  path('api/', include('market.urls')),
  path('api/', include('catalog.urls')),
  path('api/', include('epc.urls')),
  path('api/', include('governance.urls')),
  path('api/', include('consulting.urls')),
  path('api/', include('finance.urls')),
]


