from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSignupSerializer(serializers.ModelSerializer):
    """회원가입용 시리얼라이저"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    name = serializers.CharField(required=True, source='first_name')

    class Meta:
        model = User
        fields = [
            'username', 'password', 'email', 'name',
            'phone', 'birth', 'gender'
        ]
        extra_kwargs = {
            'email': {'required': False},
            'phone': {'required': True},
            'birth': {'required': False},
            'gender': {'required': False},
        }

    def validate_username(self, value):
        """아이디 유효성 검사"""
        if len(value) < 4 or len(value) > 20:
            raise serializers.ValidationError("아이디는 4-20자로 입력해주세요.")

        if not value.isalnum():
            raise serializers.ValidationError("아이디는 영문과 숫자만 사용 가능합니다.")

        return value

    def validate_phone(self, value):
        """전화번호 유효성 검사"""
        # 숫자만 추출
        phone_digits = ''.join(filter(str.isdigit, value))

        if len(phone_digits) < 10 or len(phone_digits) > 11:
            raise serializers.ValidationError("올바른 전화번호를 입력해주세요.")

        return phone_digits

    def create(self, validated_data):
        """사용자 생성"""
        # name 필드를 first_name으로 매핑
        first_name = validated_data.pop('first_name', '')

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=first_name,
            phone=validated_data.get('phone', ''),
            birth=validated_data.get('birth'),
            gender=validated_data.get('gender', ''),
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    """사용자 정보 조회용 시리얼라이저"""
    name = serializers.CharField(source='first_name', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'name',
            'phone', 'birth', 'gender', 'disability_type',
            'created_at'
        ]
        read_only_fields = ['id', 'username', 'created_at']


class UserLoginSerializer(serializers.Serializer):
    """로그인용 시리얼라이저"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
