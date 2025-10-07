from rest_framework.routers import DefaultRouter
from .views import CommunityEnergyViewSet, VotingViewSet

router = DefaultRouter()
router.register(r'ce', CommunityEnergyViewSet)
router.register(r'votaciones', VotingViewSet)

urlpatterns = router.urls





