from django.contrib import admin
from blog_api.models import *


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostImages)
admin.site.register(Comment)
admin.site.register(Likes)
