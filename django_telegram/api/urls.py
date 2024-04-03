from django.urls import path

import api.views

urlpatterns = [
    path(
        "tests/",
        api.views.TestViewSet.as_view({"get": "list"}),
        name="tests",
    ),
    path(
        "questions/<int:test>/",
        api.views.QuestionViewSet.as_view({"get": "list"}),
        name="questions_test",
    ),
]
