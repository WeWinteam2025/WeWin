from rest_framework.routers import DefaultRouter
from .views import EnergyOfferViewSet, EnergyDemandViewSet

router = DefaultRouter()
router.register(r'offers', EnergyOfferViewSet)
router.register(r'demands', EnergyDemandViewSet)

urlpatterns = router.urls





