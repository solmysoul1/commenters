import logging
from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from movies.models import Review, Movie, Comment
User = get_user_model()

# django 로거를 가져옵니다.
logger = logging.getLogger(__name__)

class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'

class CustomRegisterSerializer(RegisterSerializer):
    # 기본 설정 필드: username, password, email
    # 추가 설정 필드: nickname
    nickname = serializers.CharField(max_length=50)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', '')
        return data

class FollowSerializer(serializers.ModelSerializer):
    
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'username', 'nickname')
        
    followings = UserSerializer(many=True, read_only=True)
    followers = UserSerializer(many=True, read_only=True)

    followings_count = serializers.IntegerField(
        source='followings.count', 
        read_only=True
    )

    followers_count = serializers.IntegerField(
        source='followers.count', 
        read_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'followings', 'nickname', 'followers', 'followings_count', 'followers_count')

class ProfileSerializer(UserDetailsSerializer):

    class UserReviewListSerializer(serializers.ModelSerializer):
        
        class MovieSerializer(serializers.ModelSerializer):
            class Meta:
                model = Movie
                fields = '__all__'

        movie = MovieSerializer(read_only=True)

        class CommentSerializer(serializers.ModelSerializer):
            class Meta:
                model = Comment
                fields = '__all__'

        comment_set = CommentSerializer(read_only=True, many=True)
        comment_set_count = serializers.IntegerField(
            source='comment_set.count', 
            read_only=True
        )

        class UserSerializer(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = '__all__'
        
        like_users = UserSerializer(many=True, read_only=True)
        like_users_count = serializers.IntegerField(
            source='like_users.count', 
            read_only=True
        )
        
        class Meta:
            model = Review
            fields = '__all__'

    review_set = UserReviewListSerializer(many=True, read_only=True)

    class FollowerSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'nickname',)
    
    followings = FollowerSerializer(many=True, read_only=True)
    followers = FollowerSerializer(many=True, read_only=True)

    followings_count = serializers.IntegerField(
        source='followings.count', 
        read_only=True
    )

    followers_count = serializers.IntegerField(
        source='followers.count', 
        read_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'nickname', 'email', 'followings', 'followers', 'followings_count', 'followers_count', 'review_set')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'