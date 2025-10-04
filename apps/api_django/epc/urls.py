from rest_framework.routers import DefaultRouter
from .views import WorkOrderViewSet, RoofListingViewSet, QuoteViewSet

router = DefaultRouter()
router.register(r'workorders', WorkOrderViewSet)
router.register(r'roof/list', RoofListingViewSet)
router.register(r'quote', QuoteViewSet)

urlpatterns = router.urls


