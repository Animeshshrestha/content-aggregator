from django.urls import path, include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('user-signup', views.UserCreate)
router.register('news', views.NewsViewsSet)

urlpatterns =[
    path('', include(router.urls)),
]