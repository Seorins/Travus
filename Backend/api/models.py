from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class TravelSpotCategory(models.Model):
    """여행지 카테고리"""
    name = models.CharField(max_length=50, unique=True, verbose_name='카테고리명')
    description = models.TextField(blank=True, null=True, verbose_name='설명')
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name='아이콘')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        db_table = 'travel_spot_categories'
        verbose_name = '여행지 카테고리'
        verbose_name_plural = '여행지 카테고리'

    def __str__(self):
        return self.name


class TravelSpot(models.Model):
    """여행지 정보"""
    # 공공데이터 API 필드
    content_id = models.CharField(max_length=50, unique=True, verbose_name='콘텐츠 ID')
    content_type_id = models.CharField(max_length=20, verbose_name='콘텐츠 타입 ID')

    # 기본 정보
    name = models.CharField(max_length=200, verbose_name='여행지명')
    category = models.ForeignKey(
        TravelSpotCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='travel_spots',
        verbose_name='카테고리'
    )

    # 위치 정보
    address = models.CharField(max_length=300, verbose_name='주소')
    area_code = models.CharField(max_length=10, blank=True, null=True, verbose_name='지역코드')
    sigungu_code = models.CharField(max_length=10, blank=True, null=True, verbose_name='시군구코드')
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True,
        verbose_name='위도'
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True,
        verbose_name='경도'
    )

    # 상세 정보
    description = models.TextField(blank=True, null=True, verbose_name='설명')
    overview = models.TextField(blank=True, null=True, verbose_name='개요')
    tel = models.TextField(blank=True, null=True, verbose_name='전화번호')
    tel_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='전화번호명')
    homepage = models.TextField(blank=True, null=True, verbose_name='홈페이지')
    zipcode = models.CharField(max_length=10, blank=True, null=True, verbose_name='우편번호')
    addr1 = models.CharField(max_length=300, blank=True, null=True, verbose_name='주소')
    addr2 = models.CharField(max_length=300, blank=True, null=True, verbose_name='상세주소')

    # 이미지
    image_url = models.URLField(blank=True, null=True, verbose_name='대표 이미지 URL')
    thumbnail_url = models.URLField(blank=True, null=True, verbose_name='썸네일 이미지 URL')

    # API 추가 정보
    created_time = models.CharField(max_length=20, blank=True, null=True, verbose_name='API 등록일')
    modified_time = models.CharField(max_length=20, blank=True, null=True, verbose_name='API 수정일')
    cpyrht_div_cd = models.CharField(max_length=20, blank=True, null=True, verbose_name='저작권 유형')
    cat1 = models.CharField(max_length=10, blank=True, null=True, verbose_name='대분류')
    cat2 = models.CharField(max_length=10, blank=True, null=True, verbose_name='중분류')
    cat3 = models.CharField(max_length=10, blank=True, null=True, verbose_name='소분류')
    mlevel = models.CharField(max_length=10, blank=True, null=True, verbose_name='Map Level')

    # 평점 및 통계
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(5.00)],
        verbose_name='평점'
    )
    review_count = models.IntegerField(default=0, verbose_name='리뷰 수')
    view_count = models.IntegerField(default=0, verbose_name='조회수')
    bookmark_count = models.IntegerField(default=0, verbose_name='북마크 수')

    # 메타 정보
    is_active = models.BooleanField(default=True, verbose_name='활성화 여부')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    last_synced_at = models.DateTimeField(null=True, blank=True, verbose_name='마지막 동기화')

    class Meta:
        db_table = 'travel_spots'
        verbose_name = '여행지'
        verbose_name_plural = '여행지'
        indexes = [
            models.Index(fields=['content_id']),
            models.Index(fields=['area_code', 'sigungu_code']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.name


class AccessibilityInfo(models.Model):
    """무장애 관광 정보"""
    travel_spot = models.OneToOneField(
        TravelSpot,
        on_delete=models.CASCADE,
        related_name='accessibility',
        verbose_name='여행지'
    )

    # 접근성 정보 (공공데이터 API 기반)
    parking = models.BooleanField(default=False, verbose_name='장애인 주차장')
    route = models.BooleanField(default=False, verbose_name='대중교통 접근')
    public_transport = models.BooleanField(default=False, verbose_name='무장애 이동경로')
    restroom = models.BooleanField(default=False, verbose_name='장애인 화장실')
    wheelchair = models.BooleanField(default=False, verbose_name='휠체어 대여')
    exit = models.BooleanField(default=False, verbose_name='출입통로')
    elevator = models.BooleanField(default=False, verbose_name='승강기')
    audio_guide = models.BooleanField(default=False, verbose_name='음성안내')

    # 상세 설명
    parking_info = models.TextField(blank=True, null=True, verbose_name='주차 정보')
    route_info = models.TextField(blank=True, null=True, verbose_name='이동경로 정보')
    restroom_info = models.TextField(blank=True, null=True, verbose_name='화장실 정보')
    wheelchair_info = models.TextField(blank=True, null=True, verbose_name='휠체어 정보')
    exit_info = models.TextField(blank=True, null=True, verbose_name='출입구 정보')
    elevator_info = models.TextField(blank=True, null=True, verbose_name='승강기 정보')

    # 기타 정보
    braile_block = models.BooleanField(default=False, verbose_name='점자블록')
    help_dog = models.BooleanField(default=False, verbose_name='안내견 동반')
    guide_system = models.BooleanField(default=False, verbose_name='유도 안내 설비')

    # 청각장애 정보
    sign_guide = models.BooleanField(default=False, verbose_name='수화 안내')
    video_guide = models.BooleanField(default=False, verbose_name='자막 비디오 가이드')
    hearing_room = models.BooleanField(default=False, verbose_name='청각장애 객실')

    # 추가 접근성 정보
    stroller = models.BooleanField(default=False, verbose_name='유모차 접근 가능')
    lactation_room = models.BooleanField(default=False, verbose_name='수유실')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        db_table = 'accessibility_info'
        verbose_name = '무장애 정보'
        verbose_name_plural = '무장애 정보'

    def __str__(self):
        return f"{self.travel_spot.name} 접근성 정보"


class Bookmark(models.Model):
    """북마크"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        verbose_name='사용자'
    )
    travel_spot = models.ForeignKey(
        TravelSpot,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        verbose_name='여행지'
    )
    memo = models.TextField(blank=True, null=True, verbose_name='메모')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        db_table = 'bookmarks'
        verbose_name = '북마크'
        verbose_name_plural = '북마크'
        unique_together = [['user', 'travel_spot']]
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.travel_spot.name}"


class Course(models.Model):
    """여행 코스"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name='사용자'
    )
    title = models.CharField(max_length=200, verbose_name='코스 제목')
    description = models.TextField(blank=True, null=True, verbose_name='설명')

    # 코스 메타 정보
    total_distance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='총 거리(km)'
    )
    estimated_duration = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='예상 소요시간(분)'
    )

    # 공개 설정
    is_public = models.BooleanField(default=False, verbose_name='공개 여부')
    like_count = models.IntegerField(default=0, verbose_name='좋아요 수')
    view_count = models.IntegerField(default=0, verbose_name='조회수')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        db_table = 'courses'
        verbose_name = '여행 코스'
        verbose_name_plural = '여행 코스'
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['-like_count']),
        ]

    def __str__(self):
        return self.title


class CourseSpot(models.Model):
    """코스 내 여행지"""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='course_spots',
        verbose_name='코스'
    )
    travel_spot = models.ForeignKey(
        TravelSpot,
        on_delete=models.CASCADE,
        related_name='course_spots',
        verbose_name='여행지'
    )
    order = models.IntegerField(verbose_name='순서')
    memo = models.TextField(blank=True, null=True, verbose_name='메모')
    stay_duration = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='체류 시간(분)'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        db_table = 'course_spots'
        verbose_name = '코스 여행지'
        verbose_name_plural = '코스 여행지'
        unique_together = [['course', 'travel_spot']]
        ordering = ['order']
        indexes = [
            models.Index(fields=['course', 'order']),
        ]

    def __str__(self):
        return f"{self.course.title} - {self.order}. {self.travel_spot.name}"


class Review(models.Model):
    """리뷰"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='사용자'
    )
    travel_spot = models.ForeignKey(
        TravelSpot,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='여행지'
    )

    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='평점'
    )
    content = models.TextField(verbose_name='내용')

    # 접근성 평가
    accessibility_rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='접근성 평점'
    )

    # 이미지
    images = models.JSONField(default=list, blank=True, verbose_name='이미지 URL 목록')

    # 통계
    like_count = models.IntegerField(default=0, verbose_name='좋아요 수')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        db_table = 'reviews'
        verbose_name = '리뷰'
        verbose_name_plural = '리뷰'
        indexes = [
            models.Index(fields=['travel_spot', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.travel_spot.name} ({self.rating}점)"
