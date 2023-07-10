from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DeckViewSet, CardViewSet, TagViewSet, TagToCardViewSet, PDFUploadView,DeckHistoryViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'flash-card/decks', DeckViewSet, basename='deck')
router.register(r'flash-card/deck-history', DeckHistoryViewSet, basename='deckHistory')
router.register(r'flash-card/cards', CardViewSet, basename='card')
router.register(r'flash-card/tags', TagViewSet, basename='tag')
router.register(r'flash-card/tagtocards', TagToCardViewSet, basename='tagtocard')


urlpatterns = [
    path('', include(router.urls)),
    path('flash-card/uploading-pdf', PDFUploadView.as_view()),
]
