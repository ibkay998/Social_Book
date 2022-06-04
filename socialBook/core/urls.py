from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/',views.upload,name='upload'),
    path('follow/',views.follow,name='follow'),
    path('like-post/',views.like_post,name='like-post'),
    path('profile/<str:pk>/',views.profile,name='profile'),
    path('settings/',views.settings,name='settings'),
    path('login/',views.login,name="login"),
    path('register/',views.register,name="register"),
    path('logout/',views.logout,name="logout"),
]

