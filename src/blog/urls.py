from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.Index.as_view(), name="list"),
    path("detail/<int:pk>/", views.PostDetail.as_view(), name="detail"),
    path("detail/<int:pk>/edit/", views.PostUpdate.as_view(), name="edit"),
    path("detail/<int:pk>/delete/", views.PostDelete.as_view(), name="delete"),
    path("detail/<int:pk>/comment/write/", views.CommentWrite.as_view(), name="cm-write"),
    path("detail/comment/<int:pk>/delete/", views.CommentDelete.as_view(), name="cm-delete"),
    path("search/", views.Search.as_view(), name="search"),
    path("tag-search/", views.TagSearch.as_view(), name="tag-search"),
    path("write/", views.PostWrite.as_view(), name="write"),
]
