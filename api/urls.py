from django.urls import path
from api import views

urlpatterns = [
    path('users/', views.ListUsers.as_view()),
    path('usersList/', views.UsersList.as_view()),
    path('post/new/', views.CreatePost.as_view()),
    path('post/<int:pk>/', views.PostDetail.as_view()),
    path('post/<int:pk>/edit/', views.PostEdit.as_view()),
    path('post/<int:pk>/delete/', views.DeletePost.as_view())
]