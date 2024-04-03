from rest_framework import generics, viewsets

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
