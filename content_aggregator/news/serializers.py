from django.core.validators import RegexValidator, MinLengthValidator
from django.conf import settings
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from rest_framework.exceptions import ParseError

from news.models import News

class UserCreateSerializer(serializers.ModelSerializer):

    user_news_choices = serializers.ReadOnlyField()
    confirm_password = serializers.CharField(write_only=True,
                                            required = True, 
                                            style = {'input_type': 'password', 'placeholder': 'Confirm Password'},
                                            error_messages = {"blank": "This field is required"})
    class Meta:

        model = get_user_model()
        fields = ['id','email','username','last_login','date_joined','password','confirm_password','user_news_choices']
        extra_kwargs = {
                'password':{
                'write_only':True,
                'style':{'input_type': 'password', 'placeholder': 'Password'}
            },
            'confirm_password':{
                'write_only':True
            },
            'last_login':{
                'read_only':True
            },
            'date_joined':{
                'read_only':True
            }
        }
    
    def validate_email(self, data):

        if data is None or data == '':
            raise serializers.ValidationError("This field is required.") 
        try:
            get_user_model().objects.get(email=data)
            raise serializers.ValidationError("Account cannot be created - An account with this email already exists; please login.")
        except ObjectDoesNotExist:
            pass
        return data

class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ['id','title','link','description','images_link','category']


