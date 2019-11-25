from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Modify the Admin page for questions"""
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes':['collapse']}),
        ('Survey', {'fields': ['survey']})
        ]
    inlines = [ChoiceInline]

    list_display = ('question_text', 'pub_date', 'was_published_recently', 'survey')

    list_filter = ['pub_date', "survey"]

    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
admin.site.unregister(Group)
