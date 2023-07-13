from django.urls import path
from bookmarks import views

urlpatterns = [
    path('bookmarks/', views.bookmarks_list),
    path('bookmarks/<str:url>/', views.bookmark_controller),

]
