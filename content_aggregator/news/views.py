import os

from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.core.paginator import Paginator

from .custom_auth import EmailBackend
from .forms import CustomUserForm, UserLoginForm, UserNewsCategory
from .models import UserExtended, News

def logout_view(request):

	logout(request)
	return redirect('user-login')

class UserSignUpView(View):

    template_name = 'user_signup.html'

    def get(self, request):
        form = CustomUserForm(None)
        return render(request, self.template_name, {'form':form})

    def post(self,request):

        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('user-email')
        return render(request, self.template_name,{'form':form})

class UserLoginView(View, EmailBackend):

    template_name = 'user_login.html'

    def get(self, request):

        form = UserLoginForm(None)
        return render(request, self.template_name, {'form':form})

    def post(self, request):

        form = UserLoginForm(request.POST)

        if form.is_valid():
            user_email = request.POST.get('email')
            password = request.POST.get('password')

            user = self.authenticate(request,email=user_email, password=password)

            if user is not None:

                login(request, user)
                return redirect('user-news-list')

            messages.error(request,"Invalid user/email combination")
            return render(request, self.template_name, {'form':form})	
        return render(request, self.template_name,{'form':form})

class NewsView(View):
    template_name = 'news.html'

    def user_news_choice(self, request):

        user_choices = request.user.user_news_choices

        if user_choices:
            my_filter_qs = Q()
            for news  in user_choices:
                my_filter_qs = my_filter_qs | Q(category=news)
            return my_filter_qs
        return user_choices

    def get(self, request):

        user_news = self.user_news_choice(request)
        if user_news:
            news_query = News.objects.filter(user_news).order_by('?')
            data = {'user_news_choice':request.user.user_news_choices}
            form = UserNewsCategory(initial=data)
        else:
            news_query = News.objects.order_by('?').all()
            form = UserNewsCategory(None)

        paginator = Paginator(news_query, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'page_obj': page_obj, 'form':form})

class UserNewsSelection(LoginRequiredMixin, View):

    def post(self, request):

        data = request.POST.getlist('news_selection[]')
        print(request.POST)
        if not data:
            return JsonResponse({"error_msg":"Need to select one"}, safe=False, status=400)
        user = request.user
        user.news_choices = data
        user.save()
        return JsonResponse({"sucess_msg":"Updated Sucessfully"}, safe=False)







