from django.urls import path

from . import views

""" Map views to urls for the polls app (/polls))"""

app_name = 'polls'
urlpatterns = [
    # url: /polls
    path('', views.IndexView.as_view(), name='index'),
    # path: /polls/question_id/   f.e. /polls/5/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path: /polls/question_id/results/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # path: /polls/question_id/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    # path: /polls/about      (just some information out of the readme.md)
    path("about/", views.about, name="about"),
    # path: /polls/all_questions
    path("questions/", views.QuestionView.as_view(), name="questions"),
    # path: /polls/survey
    path("survey/", views.SurveyView.as_view(), name="survey"),
    # path: /polls/survey/question_id/vote
    path("survey/<int:question_id>/vote/", views.survey_vote, name="survey_vote"),
    # path: /polls/survey_result
    path("survey/survey_result", views.SurveyResultView.as_view(), name="survey_result")
]
