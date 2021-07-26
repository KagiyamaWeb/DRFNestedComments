from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/new/', views.PostNew.as_view(), name='post_new'),
    #path('post/<str:user>', views.user_posts, name='user_posts'),
    #path('subscribe/<str:username>', views.Subscribe.as_view(), name='subscribe'),
]