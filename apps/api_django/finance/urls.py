from rest_framework.routers import DefaultRouter
from .views import WalletViewSet, MovementViewSet, SettlementViewSet, InvestmentViewSet

router = DefaultRouter()
router.register(r'wallets', WalletViewSet)
router.register(r'movements', MovementViewSet)
router.register(r'settlements', SettlementViewSet)
router.register(r'investments', InvestmentViewSet, basename='investments')

urlpatterns = router.urls


