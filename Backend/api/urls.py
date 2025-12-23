from django.urls import path, include
from .views import analyze_image, chat_ai
from rest_framework.routers import DefaultRouter
from .views import (
    TravelSpotViewSet, TravelSpotCategoryViewSet,
    BookmarkViewSet, CourseViewSet, ReviewViewSet,
    SignupView, LoginView, LogoutView, MeView, CheckUsernameView,
    CourseCommentListCreateView, CourseCommentDetailView, CourseCommentRepliesView
)

router = DefaultRouter()
router.register(r'travel-spots', TravelSpotViewSet, basename='travel-spot')
router.register(r'categories', TravelSpotCategoryViewSet, basename='category')
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'reviews', ReviewViewSet, basename='review')

# 인증 관련 기능 auth로 묶음
urlpatterns = [
    path('', include(router.urls)),
    path('auth/check-username/', CheckUsernameView.as_view(), name='check-username'),
    path('auth/signup/', SignupView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('auth/me/', MeView.as_view()),

    # 코스 댓글 API
    path('courses/<int:course_id>/comments/', CourseCommentListCreateView.as_view(), name='course-comment-list'),
    path('comments/<int:pk>/', CourseCommentDetailView.as_view(), name='course-comment-detail'),
    path('comments/<int:comment_id>/replies/', CourseCommentRepliesView.as_view(), name='course-comment-replies'),
]

