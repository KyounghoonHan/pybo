from django.contrib import admin

# Register your models here.
from . models import Question

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ["subject"]


admin.site.register(Question, QuestionAdmin)

# class QuestionAdmin(admin.ModelAdmin):
#     search_field = ["subject"]

# admin.site.register(Question, QuestionAdmin)
