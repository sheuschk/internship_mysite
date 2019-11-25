from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from .models import Choice, Question
from . import forms
# Create your views here.


class IndexView(generic.ListView):
    """Generic view over the latest five questions"""
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """ Return the last five published questions"""
        questions = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
        return questions


class DetailView(generic.DetailView):
    """Generic view about the details for one question"""
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet"""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """View to show the results of a question"""
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet"""
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    """Controls if a choice is selected and logs a new vote for a question into a db"""
    question = get_object_or_404(Question, pk=question_id)
    try:
        # race condition here by adding a vote to the score
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            "error_message": "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # The redirect prevents data from being posted twice if the user hits the back button
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class QuestionView(generic.ListView):
    """A view which displays all questions in a list"""
    model = Question
    template_name = "polls/questions.html"
    context_object_name = "all_questions_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class SurveyView(generic.ListView):
    """Displays all questions which are currently tagged as part of the survey"""
    model = Question
    template_name = "polls/survey.html"
    context_object_name = "survey_question_list"

    def get_queryset(self):
        return Question.objects.filter(survey=True, pub_date__lte=timezone.now()).order_by('-pub_date')


def survey_vote(request, question_id):
    """View which calculates the votes for a survey question and redirects to the survey"""
    question = get_object_or_404(Question, id=question_id, survey=True)
    questions = get_list_or_404(Question, survey=True)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/survey.html', {
            'survey_question_list': questions,
            "error_message": "You didn't answer every question"
        })
    else:
        messages.info(request, 'You voted for: ' + question.__str__())
        selected_choice.votes += 1
        selected_choice.save()

    return HttpResponseRedirect(reverse('polls:survey'))


class SurveyResultView(generic.ListView):
    """Shows the results of all survey questions"""
    model = Question
    template_name = "polls/survey_result.html"
    context_object_name = 'survey_result_list'

    def get_queryset(self):
        return Question.objects.filter(survey=True, pub_date__lte=timezone.now()).order_by('-pub_date')


def about(request):
    """Renders a template for information about the application """
    return render(request, "polls/about.html")



