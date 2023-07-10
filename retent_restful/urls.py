from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DeckViewSet, CardViewSet, TagViewSet, TagToCardViewSet, PDFUploadView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'flash-card/decks', DeckViewSet)
router.register(r'flash-card/cards', CardViewSet)
router.register(r'flash-card/tags', TagViewSet)
router.register(r'flash-card/tagtocards', TagToCardViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('flash-card/uploding-pdf', PDFUploadView.as_view()),
]
