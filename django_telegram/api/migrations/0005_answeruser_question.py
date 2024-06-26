# Generated by Django 4.2.9 on 2024-04-04 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_answeruser"),
    ]

    operations = [
        migrations.AddField(
            model_name="answeruser",
            name="question",
            field=models.ForeignKey(
                default=1,
                help_text="выберите вопрос",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ansusers",
                related_query_name="ansusers",
                to="api.question",
                verbose_name="вопрос",
            ),
            preserve_default=False,
        ),
    ]
