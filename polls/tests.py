import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


def create_question(question_text, days, survey=False):
    """ Simple function to create a question"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time, survey=survey)


class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        as_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """ was_published_recently() returns True for questions whose pub_date
        is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    """ Test Class for the Index View"""
    def test_no_questions(self):
        """Checks if no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past question.>'])

    def test_future_question(self):
        """Tests if the index contains questions which are from 30 days in the future,
         it assert that there shouldn't be one"""
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")

    def test_future_question_and_past_question(self):
        """ Even if both past and future questions exist, only past questions
        are displayed."""
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """ The questions index page may display multiple questions."""
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionDetailViewTests(TestCase):
    """A class for testing the Detail View"""

    def test_no_questions(self):
        """Checks if no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:questions'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['all_questions_list'], [])

    def test_future_question(self):
        """ The detail view of a question with a pub_date in the future
        returns a 404 not found."""
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past
        displays the question's text."""
        past_question = create_question(question_text='Past question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionResultViewTests(TestCase):
    """A class to test the Result view """

    def test_future_question(self):
        """Test that the Result View won't show any future question (ResultView.get_queryset works)"""
        future_question = create_question(question_text="Future question", days=5)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """Tests that Result View shows questions from the past"""
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question)


class QuestionViewTests(TestCase):
    """A class to test the view which shows every question"""

    def test_no_questions(self):
        """Test that a message for missing polls is displayed"""
        response = self.client.get(reverse('polls:questions'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['all_questions_list'], [])

    def test_future_question(self):
        """Test that the Result View won't show any future question (ResultView.get_queryset works)"""
        create_question(question_text="Future question", days=5)
        url = reverse("polls:questions")
        response = self.client.get(url)
        self.assertContains(response, "No polls are available.")

    def test_past_question(self):
        """Tests that Result View shows questions from the past"""
        create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:questions")
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['all_questions_list'], ['<Question: Past Question.>'])


class SurveyViewTests(TestCase):
    """Tests for the view which displays the survey"""

    def test_no_question(self):
        """Test that a message for missing polls is displayed"""
        response = self.client.get(reverse('polls:survey'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry no survey right now.")
        self.assertQuerysetEqual(response.context['survey_question_list'], [])

    def test_no_survey_question(self):
        """Test that a message for missing survey polls is displayed"""
        create_question(question_text='No survey Question', days=-5)
        response = self.client.get(reverse('polls:survey'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry no survey right now.")
        self.assertQuerysetEqual(response.context['survey_question_list'], [])

    def test_survey_and_no_survey_question(self):
        """Tests that just polls for the survey gets displayed"""
        create_question(question_text="No survey question.", days=-5)
        create_question(question_text="Survey question.", days=-5, survey=True)
        url = reverse("polls:survey")
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['survey_question_list'], ['<Question: Survey question.>'])

    def test_past_question(self):
        """Tests that Survey View shows questions from the past"""
        create_question(question_text="Past question.", days=-5, survey=True)
        url = reverse("polls:survey")
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['survey_question_list'], ['<Question: Past question.>'])

    def test_future_question(self):
        """Test that the Survey View won't show any future question (SurveyView.get_queryset works)"""
        create_question(question_text="Future question", days=5, survey=True)
        url = reverse("polls:survey")
        response = self.client.get(url)
        self.assertContains(response, "Sorry no survey right now.")


class SurveyResultViewTest(TestCase):
    """Tests the Survey Result View"""

    def test_past_question(self):
        """Tests that Survey Result View shows questions from the past"""
        create_question(question_text="Past question.", days=-5, survey=True)
        url = reverse("polls:survey_result")
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['survey_result_list'], ['<Question: Past question.>'])

    def test_future_question(self):
        """Test that the Survey Result View won't show any future question """
        create_question(question_text="Future question", days=5, survey=True)
        url = reverse("polls:survey_result")
        response = self.client.get(url)
        self.assertContains(response, "No survey right now.")

    def test_no_question(self):
        """Test that a message for missing polls is displayed"""
        response = self.client.get(reverse('polls:survey_result'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No survey right now.")
        self.assertQuerysetEqual(response.context['survey_result_list'], [])

    def test_no_survey_question(self):
        """Test that a message for missing survey polls is displayed"""
        create_question(question_text='No survey Question', days=-5)
        response = self.client.get(reverse('polls:survey_result'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No survey right now.")
        self.assertQuerysetEqual(response.context['survey_result_list'], [])

    def test_survey_and_no_survey_question(self):
        """Tests that just polls for the survey gets displayed"""
        create_question(question_text="No survey question.", days=-5)
        create_question(question_text="Survey question.", days=-5, survey=True)
        url = reverse("polls:survey_result")
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['survey_result_list'], ['<Question: Survey question.>'])
