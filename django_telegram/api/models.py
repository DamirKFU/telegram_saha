import django.db.models


__all__ = []


class Test(django.db.models.Model):
    name = django.db.models.CharField(
        "название",
        max_length=150,
        unique=True,
        help_text="напишите название",
    )

    def __str__(self):
        return self.name[:20]

    class Meta:
        verbose_name = "тест"
        verbose_name_plural = "тесты"


class Question(django.db.models.Model):
    test = django.db.models.ForeignKey(
        Test,
        on_delete=django.db.models.CASCADE,
        verbose_name="тест",
        related_name="questions",
        related_query_name="questions",
        help_text="выберите тест",
    )
    text = django.db.models.CharField(
        "текст вопроса",
        max_length=100,
    )
    number = django.db.models.IntegerField(
        "номер теста",
        unique=True,
    )

    def __str__(self):
        return self.text[:30]

    class Meta:
        verbose_name = "вопрос"
        verbose_name_plural = "вопросы"


class Answer(django.db.models.Model):
    question = django.db.models.ForeignKey(
        Question,
        on_delete=django.db.models.CASCADE,
        verbose_name="вопрос",
        related_name="answers",
        related_query_name="answers",
        help_text="выберите вопрос",
    )
    text = django.db.models.CharField(
        "текст ответа",
        max_length=100,
    )
    ball = django.db.models.PositiveIntegerField(
        "количество балов",
        default=0,
    )

    class Meta:
        verbose_name = "ответ"
        verbose_name_plural = "ответы"


class AnswerUser(django.db.models.Model):
    user = django.db.models.IntegerField(
        "номер теста",
    )
    answer = django.db.models.ForeignKey(
        Answer,
        on_delete=django.db.models.CASCADE,
        verbose_name="ответ",
        related_name="ansusers",
        related_query_name="ansusers",
        help_text="выберите ответ",
    )
    question = django.db.models.ForeignKey(
        Question,
        on_delete=django.db.models.CASCADE,
        verbose_name="вопрос",
        related_name="ansusers",
        related_query_name="ansusers",
        help_text="выберите вопрос",
    )

    class Meta:
        verbose_name = "ответ пользователя"
        verbose_name_plural = "ответы пользователя"
        unique_together = (
            "user",
            "answer",
        )
