from django.contrib import admin
from .models.course import * 
from .models.college import * 
from .models.country import * 
from .models.blog import * 
# Register your models here.
admin.site.register(Country)
admin.site.register(College)
admin.site.register(CourseType)
admin.site.register(Course)
admin.site.register(Blog)
admin.site.register(BlogComment)
admin.site.register(CommentReply)
admin.site.register(BlogLike)
admin.site.register(SavedBlog)