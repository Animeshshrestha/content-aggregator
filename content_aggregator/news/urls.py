from django.urls import path

from .views import *

urlpatterns = [
    path('signup/',UserSignUpView.as_view(), name='user-signup'),
    path('login/',UserLoginView.as_view(), name='user-login'),
    path('news-list/', NewsView.as_view(), name='user-news-list'),
    path('news-selection/', UserNewsSelection.as_view(), name='user-news-selection'),
    path('logout/', logout_view, name='user-logout'),
]