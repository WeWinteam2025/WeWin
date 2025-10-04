from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, B2BOrderViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'order', B2BOrderViewSet)

urlpatterns = router.urls


