from django.contrib import admin
from .models import Category, Question, Answer, QuizAttempt


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ['text', 'category', 'difficulty', 'created_by']
    list_filter = ['category', 'difficulty']
    search_fields = ['text']


admin.site.register(Category)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(QuizAttempt)
