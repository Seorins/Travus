from rest_framework import serializers
from .models import (
    TravelSpotCategory, TravelSpot, AccessibilityInfo,
    Bookmark, Course, CourseSpot, Review
)
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

User = get_user_model()


class TravelSpotCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelSpotCategory
        fields = ['id', 'name', 'description', 'icon', 'created_at']


class AccessibilityInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessibilityInfo
        fields = [
            'id', 'parking', 'route', 'public_transport', 'restroom',
            'wheelchair', 'exit', 'elevator', 'audio_guide',
            'parking_info', 'route_info', 'restroom_info',
            'wheelchair_info', 'exit_info', 'elevator_info',
            'braile_block', 'help_dog', 'guide_system',
            'stroller', 'lactation_room'
        ]


class TravelSpotListSerializer(serializers.ModelSerializer):
    """여행지 리스트용 Serializer (간단한 정보)"""
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = TravelSpot
        fields = [
            'id', 'content_id', 'name', 'category', 'category_name',
            'address', 'area_code', 'image_url', 'thumbnail_url',
            'rating', 'review_count', 'view_count', 'bookmark_count'
        ]


class TravelSpotDetailSerializer(serializers.ModelSerializer):
    """여행지 상세 정보용 Serializer"""
    category = TravelSpotCategorySerializer(read_only=True)
    accessibility = AccessibilityInfoSerializer(read_only=True)

    class Meta:
        model = TravelSpot
        fields = [
            'id', 'content_id', 'content_type_id', 'name', 'category',
            'address', 'area_code', 'sigungu_code', 'latitude', 'longitude',
            'description', 'tel', 'homepage',
            'image_url', 'thumbnail_url',
            'rating', 'review_count', 'view_count', 'bookmark_count',
            'accessibility', 'is_active', 'created_at', 'updated_at'
        ]


class BookmarkSerializer(serializers.ModelSerializer):
    travel_spot = TravelSpotListSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = ['id', 'travel_spot', 'memo', 'created_at']


class CourseSpotSerializer(serializers.ModelSerializer):
    travel_spot = TravelSpotListSerializer(read_only=True)

    class Meta:
        model = CourseSpot
        fields = ['id', 'travel_spot', 'order', 'memo', 'stay_duration']


class CourseSerializer(serializers.ModelSerializer):
    course_spots = CourseSpotSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'user', 'username', 'title', 'description',
            'total_distance', 'estimated_duration',
            'is_public', 'like_count', 'view_count',
            'course_spots', 'created_at', 'updated_at'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'username', 'travel_spot',
            'rating', 'content', 'accessibility_rating',
            'images', 'like_count', 'created_at', 'updated_at'
        ]


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "password",
            "first_name", "last_name", "phone",
            "disability_type", "preferred_accessibility",
        ]
        extra_kwargs = {
            "email": {"required": False, "allow_blank": True},
            "first_name": {"required": False, "allow_blank": True},
            "last_name": {"required": False, "allow_blank": True},
            "phone": {"required": False, "allow_blank": True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data.get("username"),
            password=data.get("password")
        )
        if not user:
            raise serializers.ValidationError("아이디 또는 비밀번호가 올바르지 않습니다.")
        data["user"] = user
        return data