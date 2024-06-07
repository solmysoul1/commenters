from rest_framework import serializers
from .models import Genre, Movie, Review, Comment
from .models import Movie, Review, Comment, Genre
from django.contrib.auth import get_user_model

User = get_user_model()

class MovieListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ('id', 'title')

class MovieSerializer(serializers.ModelSerializer):
    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = ('id', 'name')
    
    genres = GenreSerializer(read_only=True, many=True)

    class ReviewDetailSerializer(serializers.ModelSerializer):
        class CommentSerializer(serializers.ModelSerializer):
            is_mine = serializers.SerializerMethodField()

            def get_is_mine(self, obj):
                request = self.context.get('request', None)
                if request and request.user.is_authenticated and request.user == obj.user:
                    return True
                return False

            class Meta:
                model = Comment
                fields = '__all__'
        
        comment_set = CommentSerializer(read_only=True, many=True)

        class LikeUserSerializer(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = '__all__'

        like_users = LikeUserSerializer(read_only=True, many=True)
        
        like_users_count = serializers.IntegerField(
            source='like_users.count', 
            read_only=True
        )

        is_like = serializers.SerializerMethodField()

        def get_is_like(self, obj):
            request = self.context.get('request', None)
            if request and request.user.is_authenticated:
                return request.user in obj.like_users.all()
            return False
        
        is_mine = serializers.SerializerMethodField()

        def get_is_mine(self, obj):
            request = self.context.get('request', None)
            if request and request.user.is_authenticated and request.user == obj.user:
                return True
            return False
        
        class Meta:
            model = Review
            fields = '__all__'

    review_set = ReviewDetailSerializer(read_only=True, many=True)
    is_like = serializers.SerializerMethodField()

    def get_is_like(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return request.user in obj.like_users.all()
        return False
    
    is_dislike = serializers.SerializerMethodField()
    
    def get_is_dislike(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return request.user in obj.dislike_users.all()
        return False
    
    is_watch = serializers.SerializerMethodField()

    def get_is_watch(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
                return request.user in obj.watchlist_users.all()
        return False
    
    class LikeUserSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = User
            fields = ('id', 'nickname',)
    
    like_users = LikeUserSerializer(read_only=True, many=True)
    like_users_count = serializers.IntegerField(
            source='like_users.count', 
            read_only=True
        )
    
    dislike_users = LikeUserSerializer(read_only=True, many=True)
    dislike_users_count = serializers.IntegerField(
            source='dislike_users.count', 
            read_only=True
        )
    
    watch_users = LikeUserSerializer(read_only=True, many=True)
    watch_users_count = serializers.IntegerField(
            source='watchlist_users.count', 
            read_only=True
        )
    
    class Meta:
        model = Movie
        fields = '__all__'

class GenreListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'

class ReviewListSerializer(serializers.ModelSerializer):
    class MovieDetailSerializer(serializers.ModelSerializer):
        class GenreSerializer(serializers.ModelSerializer):
            class Meta:
                model = Genre
                fields = ('id', 'name')

        genres = GenreSerializer(read_only=True, many=True)
        
        class Meta:
            model = Movie
            fields = ('id', 'title', 'genres', 'runtime', 'adult', 'vote_average', 'poster_path')
    
    movie = MovieDetailSerializer(read_only=True)

    class LikeUserserializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = '__all__'

    like_users = LikeUserserializer(read_only=True, many=True)
    like_users_count = serializers.IntegerField(
        source='like_users.count', 
        read_only=True
    )
    
    class Meta:
        model = Review
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class LikeUserserializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = '__all__'

    like_users = LikeUserserializer(read_only=True, many=True)
    like_users_count = serializers.IntegerField(
        source='like_users.count', 
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'movie')

