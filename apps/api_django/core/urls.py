from rest_framework.routers import DefaultRouter
from .views import (
  OrganizationViewSet,
  ActorViewSet,
  ProjectViewSet,
  MeasurementViewSet,
  ContractViewSet,
  UserProfileViewSet,
)

router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet)
router.register(r'actors', ActorViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'measurements', MeasurementViewSet)
router.register(r'contracts', ContractViewSet)
router.register(r'profiles', UserProfileViewSet)

urlpatterns = router.urls


