from django.contrib import admin
from .models import (
    TravelSpotCategory, TravelSpot, AccessibilityInfo,
    Bookmark, Course, CourseSpot, Review
)


@admin.register(TravelSpotCategory)
class TravelSpotCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'icon', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(TravelSpot)
class TravelSpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_id', 'address', 'rating', 'view_count', 'bookmark_count', 'is_active', 'created_at')
    list_filter = ('category_id', 'is_active', 'area_code')
    search_fields = ('name', 'address', 'description', 'content_id')
    ordering = ('-created_at',)
    readonly_fields = ('content_id', 'view_count', 'bookmark_count', 'review_count', 'created_at', 'updated_at')

    fieldsets = (
        ('기본 정보', {
            'fields': ('content_id', 'content_type_id', 'name', 'category', 'description')
        }),
        ('위치 정보', {
            'fields': ('address', 'area_code', 'sigungu_code', 'latitude', 'longitude')
        }),
        ('연락처', {
            'fields': ('tel', 'homepage')
        }),
        ('이미지', {
            'fields': ('image_url', 'thumbnail_url')
        }),
        ('통계', {
            'fields': ('rating', 'review_count', 'view_count', 'bookmark_count')
        }),
        ('메타', {
            'fields': ('is_active', 'last_synced_at', 'created_at', 'updated_at')
        }),
    )


@admin.register(AccessibilityInfo)
class AccessibilityInfoAdmin(admin.ModelAdmin):
    list_display = ('travel_spot', 'parking', 'restroom', 'wheelchair', 'elevator', 'audio_guide')
    list_filter = ('parking', 'restroom', 'wheelchair', 'elevator', 'audio_guide', 'braile_block', 'help_dog')
    search_fields = ('travel_spot__name',)
    ordering = ('-created_at',)

    fieldsets = (
        ('여행지', {
            'fields': ('travel_spot',)
        }),
        ('접근성 시설', {
            'fields': ('parking', 'route', 'public_transport', 'restroom', 'wheelchair', 'exit', 'elevator', 'audio_guide')
        }),
        ('시설 상세 정보', {
            'fields': ('parking_info', 'route_info', 'restroom_info', 'wheelchair_info', 'exit_info', 'elevator_info')
        }),
        ('기타 정보', {
            'fields': ('braile_block', 'help_dog', 'guide_system', 'stroller', 'lactation_room')
        }),
    )


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'travel_spot', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'travel_spot__name')
    ordering = ('-created_at',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_public', 'like_count', 'view_count', 'created_at')
    list_filter = ('is_public', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    ordering = ('-created_at',)
    readonly_fields = ('like_count', 'view_count', 'created_at', 'updated_at')


@admin.register(CourseSpot)
class CourseSpotAdmin(admin.ModelAdmin):
    list_display = ('course', 'travel_spot', 'order', 'stay_duration', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('course__title', 'travel_spot__name')
    ordering = ('course', 'order')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'travel_spot', 'rating', 'accessibility_rating', 'like_count', 'created_at')
    list_filter = ('rating', 'accessibility_rating', 'created_at')
    search_fields = ('user__username', 'travel_spot__name', 'content')
    ordering = ('-created_at',)
    readonly_fields = ('like_count', 'created_at', 'updated_at')
