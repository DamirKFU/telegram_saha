from django.db.models import Sum
from rest_framework import generics, views, viewsets
from rest_framework import status
from rest_framework.response import Response


import api.models
import api.pagination
import api.serializers


__all__ = []


class TestViewSet(viewsets.ModelViewSet):
    queryset = api.models.Test.objects.all()
    serializer_class = api.serializers.TestSerializer


class TestListAPIView(generics.ListAPIView):
    queryset = api.models.Test.objects.all()
    serializer_class = api.serializers.TestSerializer
    pagination_class = api.pagination.StandardResultsSetPagination


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = api.models.Question.objects.all()
    serializer_class = api.serializers.QuestionSerializer

    def get_queryset(self):
        test_id = self.request.parser_context["kwargs"].get("test")
        return api.models.Question.objects.filter(
            test=test_id,
        )


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = api.models.Question.objects.all()
    serializer_class = api.serializers.AnswerSerializer
    pagination_class = None

    def get_queryset(self):
        question_id = self.request.parser_context["kwargs"].get("question")
        return api.models.Answer.objects.filter(
            question=question_id,
        )


class AnswerUserListAPIView(views.APIView):
    def get(self, request, test, user):
        query = api.models.AnswerUser.objects.filter(
            user=user,
            question__test=1,
        ).select_related("question", "question__test", "answer")
        result = query.aggregate(Sum("answer__ball"))
        return Response({"result": result["answer__ball__sum"]})


class AnswerUserDetailAPIView(views.APIView):
    def get_object(self, **kwargs):
        try:
            user = int(kwargs.get("user"))
            question = int(kwargs.get("question"))
            return api.models.AnswerUser.objects.get(
                user=user,
                question=question,
            )
        except api.models.AnswerUser.DoesNotExist:
            return None

    def get(self, request):
        instance = self.get_object(**request.data)
        serializer = api.serializers.AnswerUserDetailSerializer(
            instance=instance,
            data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
