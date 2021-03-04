from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, status, viewsets, serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ParseError, APIException
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import News
from .serializers import UserCreateSerializer, NewsSerializer

class UserCreate(viewsets.ModelViewSet):

    queryset = get_user_model().objects.all()
    serializer_class = UserCreateSerializer
    

    def list(self, request, *args, **kwargs):

        if not request.user:
            if request.user.is_superuser():
                serializer = self.get_serializer(self.queryset, many=True)
                return Response(serializer.data)
        return Response({'permission_error': 'Only Admin allowed to view userlists'}, status=401)

    def validate_password(self,*args, **kwargs):

        if kwargs['password'] != kwargs['confirm_password']:
            raise serializers.ValidationError({'password_error':"Password Does not Match"})
        return kwargs
    
    def get_user(self, user_id):
        if get_user_model().objects.filter(id = user_id).exists():
            return get_user_model().objects.filter(id = user_id).first()
        return False

    def create(self, request, *args, **kwargs):

        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():

            password = request.data.get('password')
            confirm_password = request.data.get('confirm_password')
            self.validate_password(**{'password':password,'confirm_password':confirm_password})
            user = get_user_model()(username=request.data.get('username'), \
                                    email=request.data.get('email')
                                   )
            user.set_password(password)
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'], url_path='set_news_category', permission_classes=[IsAuthenticated])
    def set_news_category(self, request, *args, **kwargs):

        data = request.data.get('news_category',[])
        if not data:
            return Response({'news_category': 'At least one is required'}, 
                              status=status.HTTP_400_BAD_REQUEST
                            )

        user = request.user
        user.news_choices = data
        user.save()

        return Response({'news_category':user.user_news_choices}, 
                        status=status.HTTP_201_CREATED
                       )

class NewsViewsSet(viewsets.ModelViewSet):

    queryset = News.objects.order_by('?').all()
    serializer_class = NewsSerializer
    permission_classes = (IsAuthenticated,)

    def user_news_choice(self, request):

        user_choices = request.user.user_news_choices

        if user_choices:
            my_filter_qs = Q()
            for news  in user_choices:
                my_filter_qs = my_filter_qs | Q(category=news)
            return my_filter_qs
        return user_choices

    def list(self, request, *args, **kwargs):

        user_news = self.user_news_choice(request)

        if user_news:
            news_query = News.objects.filter(user_news).order_by('?')
        else:
            news_query = self.get_queryset()
        queryset = self.filter_queryset(news_query)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

