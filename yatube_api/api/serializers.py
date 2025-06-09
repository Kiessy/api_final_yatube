from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Post, Group, Follow, User


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault
    )

    class Meta:
        queryset = Follow.objects.all()
        fields_val = ('user', 'following')
        message = 'Вы уже подписанны'
        validators = [UniqueTogetherValidator(
            queryset, fields_val, message
        )]
        model = Follow
        fields = '__all__'

        def validator_following(self, data):
            self.request = self.context['request']
            self.user = self.request.user
            message = 'Вы не можете подписаться'
            if self.user == data:
                raise serializers.ValidationError(message)
            return data
