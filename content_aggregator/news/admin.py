from django.contrib import admin

from .models import News, UserExtended

admin.site.register(News)
admin.site.register(UserExtended)
