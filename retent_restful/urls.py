from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DeckViewSet, CardViewSet, TagViewSet, TagToCardViewSet, PDFUploadView,DeckHistoryViewSet,KakaoLoginView


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'flash-card/decks', DeckViewSet, basename='deck')
router.register(r'flash-card/deck-history', DeckHistoryViewSet, basename='deckHistory')
router.register(r'flash-card/cards', CardViewSet, basename='card')
router.register(r'flash-card/tags', TagViewSet, basename='tag')
router.register(r'flash-card/tag-to-decks', TagToCardViewSet, basename='tagtocard')


urlpatterns = [
    path('', include(router.urls)),
    path('flash-card/uploading-pdf', PDFUploadView.as_view()), 
    # dj-rest-auth의 URL 패턴 추가
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # dj-rest-auth의 회원가입 URL 패턴 추가
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('kakao-login/', KakaoLoginView.as_view(), name='kakao-login'),

]
