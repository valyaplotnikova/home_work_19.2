from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('list/', BlogListView.as_view(), name='blog_list'),
    path('about/<int:pk>/', BlogDetailView.as_view(), name='about'),
    path('create/', BlogCreateView.as_view(), name='create_blog'),
    path('create/<int:pk>/', BlogUpdateView.as_view(), name='update_blog'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete_blog')
]