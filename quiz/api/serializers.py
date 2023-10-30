from rest_framework import serializers
from base.models import Question, Choice, Answer, Quiz, SubmittedAnswer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "text", "question", "index", "is_answer"]


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "text", "question_type", "description",
                  "date_created", "choices", "quiz"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "index", "text",
                  "question", "submission", "is_correct"]


class SubmittedAnswerSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = SubmittedAnswer
        fields = ["id", "quiz", "answers", "score"]


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    submitted_answers = SubmittedAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "date_created", "description",
                  "questions", "submitted_answers"]
