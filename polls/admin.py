from django.contrib import admin

from .models import Choice, Question, Response


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    fields = ["choice_text", "latitude", "longitude"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ["question_text", "pub_date"]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date"]
    search_fields = ["question_text"]


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ["choice", "voted_at"]
    list_filter = ["choice__question"]
    readonly_fields = ["voted_at"]
