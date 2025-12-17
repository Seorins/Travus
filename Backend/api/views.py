from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import TravelSpot, TravelSpotCategory, Bookmark, Course, Review
from .serializers import (
    TravelSpotListSerializer, TravelSpotDetailSerializer,
    TravelSpotCategorySerializer, BookmarkSerializer,
    CourseSerializer, ReviewSerializer
)
from .services.tour_api import tour_api_service


class TravelSpotViewSet(viewsets.ReadOnlyModelViewSet):
    """여행지 ViewSet"""
    queryset = TravelSpot.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TravelSpotDetailSerializer
        return TravelSpotListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # 필터링
        area_code = self.request.query_params.get('area_code')
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')

        if area_code:
            queryset = queryset.filter(area_code=area_code)
        if category:
            queryset = queryset.filter(category__name=category)
        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset.select_related('category').prefetch_related('accessibility')

    @action(detail=False, methods=['get'])
    def from_api(self, request):
        """공공데이터 API에서 직접 데이터 가져오기"""
        area_code = request.query_params.get('area_code')
        sigungu_code = request.query_params.get('sigungu_code')
        content_type_id = request.query_params.get('content_type_id')
        page_no = int(request.query_params.get('page', 1))
        num_of_rows = int(request.query_params.get('size', 20))

        result = tour_api_service.get_area_based_list(
            area_code=area_code,
            sigungu_code=sigungu_code,
            content_type_id=content_type_id,
            page_no=page_no,
            num_of_rows=num_of_rows
        )

        if result and 'response' in result:
            response_body = result['response'].get('body', {})
            items = response_body.get('items', {})

            # items가 딕셔너리이고 'item' 키가 있으면 그것을 사용
            if isinstance(items, dict) and 'item' in items:
                item_list = items['item']
            else:
                item_list = []

            return Response({
                'count': response_body.get('totalCount', 0),
                'results': item_list
            })

        return Response(
            {'error': 'API 요청 실패'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @action(detail=False, methods=['get'])
    def search_api(self, request):
        """공공데이터 API 키워드 검색"""
        keyword = request.query_params.get('keyword', '')
        area_code = request.query_params.get('area_code')
        page_no = int(request.query_params.get('page', 1))
        num_of_rows = int(request.query_params.get('size', 20))

        if not keyword:
            return Response(
                {'error': '검색어를 입력해주세요'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = tour_api_service.search_keyword(
            keyword=keyword,
            area_code=area_code,
            page_no=page_no,
            num_of_rows=num_of_rows
        )

        if result and 'response' in result:
            response_body = result['response'].get('body', {})
            items = response_body.get('items', {})

            # items가 딕셔너리이고 'item' 키가 있으면 그것을 사용
            if isinstance(items, dict) and 'item' in items:
                item_list = items['item']
            else:
                item_list = []

            return Response({
                'count': response_body.get('totalCount', 0),
                'results': item_list
            })

        return Response(
            {'error': 'API 요청 실패'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class TravelSpotCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """여행지 카테고리 ViewSet"""
    queryset = TravelSpotCategory.objects.all()
    serializer_class = TravelSpotCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookmarkViewSet(viewsets.ModelViewSet):
    """북마크 ViewSet"""
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Bookmark.objects.filter(user=self.request.user).select_related('travel_spot')
        return Bookmark.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CourseViewSet(viewsets.ModelViewSet):
    """여행 코스 ViewSet"""
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Course.objects.all()
        if self.request.user.is_authenticated:
            # 본인 코스 + 공개 코스
            queryset = queryset.filter(
                models.Q(user=self.request.user) | models.Q(is_public=True)
            )
        else:
            # 공개 코스만
            queryset = queryset.filter(is_public=True)

        return queryset.select_related('user').prefetch_related('course_spots')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    """리뷰 ViewSet"""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Review.objects.all()
        travel_spot_id = self.request.query_params.get('travel_spot')

        if travel_spot_id:
            queryset = queryset.filter(travel_spot_id=travel_spot_id)

        return queryset.select_related('user', 'travel_spot')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
