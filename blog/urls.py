from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/new/', views.PostNew.as_view(), name='post_new'),
    path('api/posts/', views.PostsAPIView.as_view(), name='post_api'),
    path('api/posts/<int:pk>', views.PostDetailAPIView.as_view()),
    #path('api/posts/<int:pk>/comments', views.CommentsDetailAPIView.as_view()),
    #path('api/posts/<int:pk>/comments3', views.ThreeLevelCommentAPIView.as_view()),
    path('api/posts/<int:pk>/comments', views.ThreeLevelCommentAPIView.as_view()),
    path('api/posts/<int:pk>/comments/<int:cpk>', views.ThirdLevelDownAPI.as_view()),

]