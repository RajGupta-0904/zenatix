from django.contrib import admin
from .models import User, BlogPost, Category, Tag, Comment

admin.site.register(User)
admin.site.register(BlogPost)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
