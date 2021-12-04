# Here's the documentation on APIview in Django Rest Framework: https://www.django-rest-framework.org/api-guide/views/
# Addtionally here's the documentation on generic views in Django Rest Framework: https://www.django-rest-framework.org/api-guide/generic-views/

from django.shortcuts import render
from rest_framework import permissions
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Post
from .serializers import UserSerializer, PostSerializer
from .permissions import IsOwnerOrReadOnly

# Create your views here.
# Class view that gets you a list of users using generic views.
class ListUsers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Example of using APIView instead of one of the generic view.
class UsersList(APIView):
    serializer_class = UserSerializer

    def get(self, request, format = None):
        # Get the data from the database
        users = User.objects.all()
        # serializer said data, the many = true is for many to many relationships.
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

# Class view that allows you to create a post using the APIView, this has a get request as well :)
class CreatePost(APIView):
    # Add this to your views:
    # More can be read at: https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    
    def get(self, request, format = None):
        # Get the data from the database
        posts = Post.objects.all()
        # serializer said data
        serializer = self.serializer_class(posts)
        return Response(serializer.data)

    def post (self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        # post requests always require a serializer.is_valid()
        if serializer.is_valid():
            serializer.save(owner = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# Class that demonstrates how to view a single post object
class PostDetail(APIView):
    serializer_class = PostSerializer
    
    def get(self, request, pk, format = None):
        # Find post based on id number
        post = Post.objects.get(pk = pk)
        # serializer said data
        serializer = self.serializer_class(post)
        return Response(serializer.data)

class PostEdit(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def put(self, request, pk, format = None):
        # use serializer on the post found
        serializer = self.serializer_class(data = request.data)
        # Editing and Creating post object always requires .is_valid
        if serializer.is_valid():
            Post.objects.filter(pk = pk).update(title = serializer.data["title"], body = serializer.data["body"])
            # This just ensures the object returned is serialized
            return Response(self.serializer_class(Post.objects.get(pk = pk)).data)

class DeletePost(APIView):
    serializer_class = PostSerializer

    def delete(self, request, pk, format = None):
        # Find post to delete
        post = Post.objects.get(pk = pk)
        # Delete said post
        post.delete()
        return Response(status=status.HTTP_202_ACCEPTED)