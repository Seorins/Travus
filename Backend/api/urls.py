from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TravelSpotViewSet, TravelSpotCategoryViewSet,
    BookmarkViewSet, CourseViewSet, ReviewViewSet
)

router = DefaultRouter()
router.register(r'travel-spots', TravelSpotViewSet, basename='travel-spot')
router.register(r'categories', TravelSpotCategoryViewSet, basename='category')
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
