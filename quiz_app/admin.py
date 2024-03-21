from django.contrib import admin
from .models import CustomUser, Quiz, Question, AnswerOption, QuizAttempt, UserAnswer

# Optional: Customize how models are displayed in the admin
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3  # Number of extra blank questions to show

class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 4  # Number of extra blank answers to show

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]  # This allows you to add questions directly from the quiz form

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerOptionInline]  # This allows you to add answer options directly from the question form

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(AnswerOption)
admin.site.register(QuizAttempt)
admin.site.register(UserAnswer)
