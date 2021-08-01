from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/new/', views.PostNew.as_view(), name='post_new'),
    path('api/posts/', views.PostsAPIView.as_view()),
    path('api/posts/<int:pk>/', views.ThreeLevelCommentAPIView.as_view()),
    path('api/posts/<int:pk>/post_new', views.PostCommentAPIView.as_view()),
    path('api/posts/<int:pk>/comments/<int:cpk>', views.ThirdLevelDownAPI.as_view()),

]