
# Register your models here.
from quiz_app.models import Quiz, Question, AnswerOption
from django.contrib import admin


class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 3  # Determines the number of empty forms to display

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerOptionInline]

admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(AnswerOption)
