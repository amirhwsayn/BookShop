from django.contrib import admin
from .models import Books, User, Token, ADS, Files, Author, Comment

# Register your models here.
admin.site.register([Books, User, Token, ADS, Files, Author, Comment])
