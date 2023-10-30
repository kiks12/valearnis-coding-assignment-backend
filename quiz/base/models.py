from django.db import models
from django.utils import timezone


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(
        max_length=1000, default="", null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)


class Question(models.Model):
    class QuestionType(models.TextChoices):
        SINGLE_ANSWER = "SA", ("Single Answer")
        MULTI_ANSWER = "MA", ("Multi Answer")

    text = models.CharField(max_length=512)
    description = models.CharField(
        max_length=1000, default="", blank=True, null=True)
    question_type = models.CharField(
        max_length=2,
        choices=QuestionType.choices,
    )
    date_created = models.DateTimeField(default=timezone.now)
    quiz = models.ForeignKey(
        Quiz,
        related_name="questions",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )


class Choice(models.Model):
    index = models.IntegerField()
    text = models.CharField(max_length=255)
    is_answer = models.BooleanField()
    question = models.ForeignKey(
        Question,
        related_name="choices",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )


class SubmittedAnswer(models.Model):
    score = models.FloatField(default=0)
    quiz = models.ForeignKey(
        Quiz,
        related_name="submitted_answers",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )


class Answer(models.Model):
    index = models.IntegerField()
    text = models.CharField(max_length=255)
    question = models.ForeignKey(
        Question,
        related_name="answers",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    submission = models.ForeignKey(
        SubmittedAnswer,
        related_name="answers",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    is_correct = models.BooleanField(default=False, blank=True, null=True)
