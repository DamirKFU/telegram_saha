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
    path(
        "answer/<int:question>/",
        api.views.AnswerViewSet.as_view({"get": "list"}),
        name="questions_test",
    ),
    path(
        "answeruser/<int:test>/<int:user>/",
        api.views.AnswerUserListAPIView.as_view(),
        name="questions_test",
    ),
    path(
        "answeruser/",
        api.views.AnswerUserDetailAPIView.as_view(),
        name="questions_test",
    ),
]
