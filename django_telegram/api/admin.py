from django.contrib import admin

import api.models


__all__ = []


class QuestionInline(admin.TabularInline):
    exclude = []
    model = api.models.Question


class AnswerInline(admin.TabularInline):
    exclude = []
    model = api.models.Answer


@admin.register(api.models.Test)
class TagAdmin(admin.ModelAdmin):
    list_display = (api.models.Test.name.field.name,)
    inlines = [
        QuestionInline,
    ]


@admin.register(api.models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (api.models.Question.text.field.name,)
    inlines = [
        AnswerInline,
    ]
