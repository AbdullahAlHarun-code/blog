from django.urls import path, include
from . import views
app_name = 'blog'
urlpatterns = [
    path('', views.post_list_view, name='post_list_view'),
    path('tag/<slug:tag_slug>/', views.post_list_view, name='post_list_by_tag'),

    #path('', views.PostListView.as_view(), name = 'post_list_view'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('facker/', views.fakerdemo, name='facker_demo'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
]
