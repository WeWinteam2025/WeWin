from rest_framework.routers import DefaultRouter
from .views import ConsultingServiceViewSet, ConsultingPackageViewSet, ConsultingContractViewSet

router = DefaultRouter()
router.register(r'consulting/services', ConsultingServiceViewSet)
router.register(r'consulting/packages', ConsultingPackageViewSet)
router.register(r'consulting/contracts', ConsultingContractViewSet)

urlpatterns = router.urls





