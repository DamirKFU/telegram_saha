from rest_framework import serializers

import api.models

__all__ = []


class TestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = api.models.Test
        fields = ["name", "id"]


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = api.models.Question
        fields = ["id", "text"]


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = api.models.Answer
        fields = ["id", "text"]
