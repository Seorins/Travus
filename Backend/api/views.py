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
    """
    여행지 ViewSet (DB 기반)

    list: 여행지 목록 조회 (페이지네이션, 필터링, 검색 지원)
    retrieve: 여행지 상세 조회
    """
    queryset = TravelSpot.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TravelSpotDetailSerializer
        return TravelSpotListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # 이미지가 있는 여행지만 (목록 조회시)
        if self.action == 'list':
            queryset = queryset.exclude(image_url__isnull=True).exclude(image_url='')

        # 필터링
        area_code = self.request.query_params.get('area_code')
        sigungu_code = self.request.query_params.get('sigungu_code')
        content_type_id = self.request.query_params.get('content_type_id')
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')

        if area_code:
            queryset = queryset.filter(area_code=area_code)
        if sigungu_code:
            queryset = queryset.filter(sigungu_code=sigungu_code)
        if content_type_id:
            queryset = queryset.filter(content_type_id=content_type_id)
        if category:
            queryset = queryset.filter(category__name=category)
        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) |
                models.Q(address__icontains=search) |
                models.Q(description__icontains=search)
            )

        # 무장애 시설 필터링
        facilities = self.request.query_params.get('facilities')
        if facilities:
            # 쉼표로 구분된 시설 목록을 파싱
            facility_list = [f.strip() for f in facilities.split(',') if f.strip()]

            # 각 시설에 대해 필터링 (AND 조건)
            for facility in facility_list:
                # accessibility__ 프리픽스를 사용하여 관련 AccessibilityInfo 필드 필터링
                filter_kwargs = {f'accessibility__{facility}': True}
                queryset = queryset.filter(**filter_kwargs)

        # 정렬 (기본: 최신순, 옵션: 인기순, 평점순)
        ordering = self.request.query_params.get('ordering', '-created_at')
        if ordering == 'popular':
            queryset = queryset.order_by('-view_count', '-bookmark_count')
        elif ordering == 'rating':
            queryset = queryset.order_by('-rating', '-review_count')
        else:
            queryset = queryset.order_by(ordering)

        return queryset.select_related('category').prefetch_related('accessibility')

    def retrieve(self, request, pk=None):
        """상세 조회 시 조회수 증가"""
        _ = pk  # URL parameter (사용하지 않지만 signature에 필요)
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_content_id(self, request):
        """
        content_id로 여행지 조회
        GET /api/travel-spots/by_content_id/?content_id=123456
        """
        content_id = request.query_params.get('content_id')

        if not content_id:
            return Response(
                {'error': 'content_id가 필요합니다'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            travel_spot = TravelSpot.objects.select_related('category').prefetch_related('accessibility').get(
                content_id=content_id,
                is_active=True
            )
            serializer = TravelSpotDetailSerializer(travel_spot)
            return Response(serializer.data)
        except TravelSpot.DoesNotExist:
            return Response(
                {'error': f'content_id({content_id})에 해당하는 여행지를 찾을 수 없습니다'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def recommendations(self, request):
        """
        같은 지역 추천 여행지
        GET /api/travel-spots/recommendations/?content_id=123456&limit=6
        """
        content_id = request.query_params.get('content_id')
        limit = int(request.query_params.get('limit', 6))

        if not content_id:
            return Response(
                {'error': 'content_id가 필요합니다'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 현재 여행지 조회
            current_spot = TravelSpot.objects.get(content_id=content_id, is_active=True)

            # 같은 지역의 관광지 (content_type_id=12) 추천
            recommendations = TravelSpot.objects.filter(
                area_code=current_spot.area_code,
                content_type_id='12',  # 관광지만
                is_active=True
            ).exclude(
                id=current_spot.id  # 현재 여행지 제외
            ).order_by('-view_count')[:limit]  # 조회수 높은 순

            serializer = TravelSpotListSerializer(recommendations, many=True)
            return Response(serializer.data)

        except TravelSpot.DoesNotExist:
            return Response(
                {'error': f'content_id({content_id})에 해당하는 여행지를 찾을 수 없습니다'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def from_api(self, request):
        # 1. content_id 확인
        content_id = request.query_params.get('content_id')
        content_type_id = request.query_params.get('content_type_id')

        # [수정] ID가 있으면 상세 조회 로직만 수행하고 종료
        if content_id:
            # contentTypeId 포함하여 조회 (안정성 향상)
            result = tour_api_service.get_detail_common(content_id, content_type_id)

            # 404 처리
            if result and result.get('status_code') == 404:
                return Response(
                    {'error': f'해당 ID({content_id})의 여행지 정보를 찾을 수 없습니다.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # 데이터를 성공적으로 가져온 경우
            if result and 'response' in result:
                response_body = result['response'].get('body', {})
                items = response_body.get('items', {})

                if isinstance(items, dict) and 'item' in items:
                    item_list = items['item']
                    # 리스트가 아니면 리스트로 감싸기 (Normalize)
                    if not isinstance(item_list, list):
                        item_list = [item_list]
                elif isinstance(items, list):
                        # items 자체가 리스트인 경우 (가끔 발생)
                        item_list = items
                else:
                    item_list = []

                # 검색 결과가 있으면 반환
                if item_list:
                    return Response({
                        'count': len(item_list),
                        'results': item_list
                    })

            # [핵심] 조회 실패 시 500 에러 반환
            return Response(
                {'error': 'Tour API 요청 실패 - 네트워크 오류 또는 서버 문제'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
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

            # items 구조 처리 강화
            item_list = []
            if items:
                if isinstance(items, dict) and 'item' in items:
                    data = items['item']
                    item_list = data if isinstance(data, list) else [data]
                elif isinstance(items, list):
                    item_list = items
            
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

    @action(detail=False, methods=['get'])
    def detail_common(self, request):
        """
        공통 정보 상세 조회 (detailCommon1 - Service1/Service2 fallback 지원)

        Query Parameters:
            - content_id (필수): 콘텐츠 ID
            - content_type_id (선택): 콘텐츠 타입 ID (12:관광지, 14:문화시설, 15:축제, 32:숙박, 39:음식점 등)
                                      제공 시 조회 안정성이 크게 향상됩니다.
        """
        content_id = request.query_params.get('content_id')
        content_type_id = request.query_params.get('content_type_id')

        if not content_id:
            return Response(
                {'error': 'content_id가 필요합니다'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = tour_api_service.get_detail_common(content_id, content_type_id)

        # 404 처리 (데이터가 존재하지 않음)
        if result and result.get('status_code') == 404:
            return Response(
                {'error': f'해당 content_id({content_id})의 상세 정보를 찾을 수 없습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # 정상 응답
        if result and 'response' in result:
            return Response(result)

        # 기타 오류 (네트워크 오류 등)
        return Response(
            {'error': 'Tour API 요청 실패 - 네트워크 오류 또는 서버 문제'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @action(detail=False, methods=['get'])
    def detail_intro(self, request):
        """소개 정보 조회 (detailIntro2)"""
        content_id = request.query_params.get('content_id')
        content_type_id = request.query_params.get('content_type_id')

        if not content_id:
            return Response(
                {'error': 'content_id가 필요합니다'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not content_type_id:
            return Response(
                {'error': 'content_type_id가 필요합니다'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = tour_api_service.get_detail_intro(content_id, content_type_id)

        if result:
            return Response(result)

        return Response(
            {'error': 'API 요청 실패'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @action(detail=False, methods=['get'])
    def detail_info(self, request):
        """반복 정보 조회 (detailInfo2)"""
        content_id = request.query_params.get('content_id')
        content_type_id = request.query_params.get('content_type_id')

        if not content_id:
            return Response(
                {'error': 'content_id가 필요합니다'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not content_type_id:
            return Response(
                {'error': 'content_type_id가 필요합니다'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = tour_api_service.get_detail_info(content_id, content_type_id)

        if result:
            return Response(result)

        return Response(
            {'error': 'API 요청 실패'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @action(detail=False, methods=['get'])
    def detail_image(self, request):
        """이미지 정보 조회 (detailImage2)"""
        content_id = request.query_params.get('content_id')

        if not content_id:
            return Response(
                {'error': 'content_id가 필요합니다'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = tour_api_service.get_detail_image(content_id)

        if result:
            return Response(result)

        return Response(
            {'error': 'API 요청 실패'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @action(detail=False, methods=['get'])
    def detail_with_tour(self, request):
        """무장애 여행정보 조회 (detailWithTour1)"""
        content_id = request.query_params.get('content_id')

        if not content_id:
            return Response(
                {'error': 'content_id가 필요합니다'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = tour_api_service.get_detail_with_tour(content_id)

        if result:
            return Response(result)

        return Response(
            {'error': 'API 요청 실패'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @action(detail=False, methods=['get'])
    def area_code(self, request):
        """지역코드 조회 (areaCode2)"""
        area_code = request.query_params.get('area_code')

        result = tour_api_service.get_area_code(area_code)

        if result:
            return Response(result)

        return Response(
            {'error': 'API 요청 실패'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @action(detail=False, methods=['get'])
    def category_code(self, request):
        """서비스분류코드 조회 (categoryCode2)"""
        content_type_id = request.query_params.get('content_type_id')
        cat1 = request.query_params.get('cat1')
        cat2 = request.query_params.get('cat2')
        cat3 = request.query_params.get('cat3')

        result = tour_api_service.get_category_code(
            content_type_id=content_type_id,
            cat1=cat1,
            cat2=cat2,
            cat3=cat3
        )

        if result:
            return Response(result)

        return Response(
            {'error': 'API 요청 실패'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @action(detail=False, methods=['get'])
    def location_based(self, request):
        """위치기반 관광정보 조회 (locationBasedList2)"""
        mapx = request.query_params.get('mapx')
        mapy = request.query_params.get('mapy')
        radius = int(request.query_params.get('radius', 1000))
        content_type_id = request.query_params.get('content_type_id')
        page_no = int(request.query_params.get('page', 1))
        num_of_rows = int(request.query_params.get('size', 20))

        if not mapx or not mapy:
            return Response(
                {'error': 'mapx와 mapy가 필요합니다'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = tour_api_service.get_location_based_list(
            mapx=mapx,
            mapy=mapy,
            radius=radius,
            content_type_id=content_type_id,
            page_no=page_no,
            num_of_rows=num_of_rows
        )

        if result and 'response' in result:
            response_body = result['response'].get('body', {})
            items = response_body.get('items', {})

            item_list = []
            if items:
                if isinstance(items, dict) and 'item' in items:
                    data = items['item']
                    item_list = data if isinstance(data, list) else [data]
                elif isinstance(items, list):
                    item_list = items

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
