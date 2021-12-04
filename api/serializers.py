# Learn more about model serializer at: https://www.django-rest-framework.org/api-guide/serializers/#modelserializer

from api.models import Post
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        # Model
        model = User
        # Fields you want serialized and returned!
        fields = ['id', 'first_name', 'last_name', 'posts']

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'owner']
    
    # def create(self, validated_data):
    #     print("Here's create method")
    #     print(validated_data)
    #     return Post.objects.create(**validated_data)

    # def create(self, validated_data):
    #     post = Post.objects.create(
    #         owner=self.context['request'].user,
    #         **validated_data
    #     )
    #     return post