from django.urls import path
from django.urls import re_path
from bookmarks import views

urlpatterns = [
    path('bookmarks/', views.bookmarks_list),
    re_path(r'^bookmarks/(?P<encoded_url>.*)/$', views.bookmark_controller),
    path('tags/', views.tags),

]
