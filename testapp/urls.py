from django.urls import path, reverse

from . import views

app_name = 'testapp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post', views.PostCreate.as_view(), name='post'),
    path('createPost', views.createPost, name='createPost'),
    path('createPost/<dept>/<id>', views.createPostFromClass, name='createPostFromClass'),
    path('course', views.course, name='course'),
    path('classsubject', views.ClassSubjectCreate.as_view(success_url = '/testapp/course'), name='classsubject'),
    path('<int:fav_id>/favorite_post', views.favorite_post, name='favorite_post'),
    path('<int:fav_id>/favorite_post_from_search', views.favorite_post_from_search, name='favorite_post_from_search'),
    path('<int:fav_id>/remove_favorite', views.remove_favorite, name='remove_favorite'),
    path('<int:fav_id>/remove_favorite_from_fav', views.remove_favorite_from_fav, name='remove_favorite_from_fav'),
    path('<int:fav_id>/remove_favorite_from_search',views.remove_favorite_from_search, name = 'remove_favorite_from_search'),
    path('favorites', views.FavoritesView.as_view(), name='favorites'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('profile/<pk>/edit', views.UpdateProfileView.as_view(), name='update_profile_view'),
    path('profile/<pk>/update', views.updateProfile, name='update_profile'),
    path('profile/<pk>/add_friend', views.addFriend, name='add_friend'),
    path('profile/<pk>/alt', views.addNewFriend.as_view(), name='add_new_friend'),
    path('threads', views.ThreadList.as_view(), name='threads'),
    path('threads/create', views.ThreadCreate.as_view(), name='thread_creation'),
    path('threads/createThread', views.createThread, name='create_thread'),
    path('threads/<pk>', views.ThreadView.as_view(), name='thread_view'),
    path('threads/<pk>/createMessage', views.createMessage, name='create_message'),
    path('post_search', views.searchView.as_view(), name='search'),
]