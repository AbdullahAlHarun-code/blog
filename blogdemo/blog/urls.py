from django.urls import path, include
from . import views
app_name = 'blog'
urlpatterns = [
    #path('', views.post_list_view, name='post_list_view'),
    path('', views.PostListView.as_view(), name = 'post_list_view'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
]
