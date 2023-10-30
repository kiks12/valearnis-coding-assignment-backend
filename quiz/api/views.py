from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status
from .serializers import ChoiceSerializer, QuestionSerializer, AnswerSerializer, QuizSerializer, SubmittedAnswerSerializer
from base.models import Quiz, Question, SubmittedAnswer


class GetQuiz(APIView):

    def get(self, request, id) -> Response:
        try:
            quiz = Quiz.objects.prefetch_related("questions").get(id=id)
            quiz_seializer = QuizSerializer(quiz)
        except:
            return Response({"error": "Record does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(quiz_seializer.data)


class ListQuizzes(APIView):

    def get(self, request) -> Response:
        quizzes = Quiz.objects.prefetch_related("questions").all()
        quizzes_serializer = QuizSerializer(quizzes, many=True)

        return Response({
            "quizzes": quizzes_serializer.data,
        })


class CreateQuiz(APIView):

    def save_question(self, question):
        serializer = QuestionSerializer(data=question)

        if serializer.is_valid():
            return [True, serializer.save()]

        return [False, serializer]

    def post(self, request):
        if "title" not in request.data or "questions" not in request.data:
            return Response({
                "error": "Invalid Data, please make sure the information is valid"
            }, status=status.HTTP_400_BAD_REQUEST)

        quiz_title = request.data.get("title")
        quiz_description = request.data.get("description")
        questions = request.data.get("questions", [])

        quiz_serializer = QuizSerializer(
            data={"title": quiz_title, "description": quiz_description})

        if quiz_serializer.is_valid():
            saved_quiz = quiz_serializer.save()

            for question in questions:
                question_data = {"text": question.get("text"), "question_type": question.get(
                    "question_type"), "description": question.get("description")}
                choices = question.get("choices", [])

                question_data['quiz'] = saved_quiz.id
                # print(question_data)
                valid, saved_question = self.save_question(question_data)

                if valid:
                    for choice in choices:
                        choice["question"] = saved_question.id
                        choice_serializer = ChoiceSerializer(data=choice)
                        if choice_serializer.is_valid():
                            choice_serializer.save()
                        else:
                            # print("INVALID CHOICE")
                            Question.objects.get(id=saved_question.id).delete()
                            Quiz.objects.get(id=saved_quiz.id).delete()
                            return Response(choice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # print("INVALID QUESTION")
                    print(saved_question.errors)
                    Quiz.objects.get(id=saved_quiz.id).delete()
                    return Response(saved_question.error_messages, status=status.HTTP_400_BAD_REQUEST)
        else:
            # print("INVALID QUIZ")
            return Response(quiz_serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "data": request.data,
            "isSuccessful": True
        })


class EvaluateQuiz(APIView):

    def compute_score(self, correct_answers, user_answers):
        total_score = 0

        for correct_answer in correct_answers:
            print(correct_answer)
            user_answers_filtered = list(filter(
                lambda x: x["question"] == correct_answer["question"], user_answers))[0]

            inner_score = 0
            for answer in correct_answer["answers"]:
                selected_answer = list(
                    filter(lambda x: x["index"] == answer["index"] and answer["is_answer"], user_answers_filtered["answers"]))

                print(selected_answer)

                if len(selected_answer) == 0:
                    continue

                inner_score += 1
                selected_answer[0]["is_correct"] = True

            if inner_score == len(correct_answer["answers"]) and inner_score != 0:
                total_score += 1

        return total_score

    def get_user_answers(self, questions) -> list:
        user_answers = []

        for question in questions:
            answers = [answer for answer in question["answer"]]
            user_answers.append({
                "question": question["question"],
                "answers": answers
            })

        return user_answers

    def get_answers(self, questions) -> list:
        answers = []

        for question in questions:
            correct_answers = [
                choice for choice in question["choices"] if choice["is_answer"]]
            answers.append({
                "question": question["id"],
                "type": question["question_type"],
                "answers": correct_answers
            })

        return answers

    # ASSUMING ALL QUESTIONS ARE REQUIRED TO BE ANSWERED

    def post(self, request):
        quiz_id = request.data.get("id")
        answers = request.data.get("userAnswers", [])

        quiz = Quiz.objects.prefetch_related("questions").get(id=quiz_id)
        serialized_quiz = QuizSerializer(quiz)

        if len(answers) != len(serialized_quiz.data['questions']):
            return Response({
                "error": "Count of answers not matching questions. Please do try again later"
            }, status=status.HTTP_400_BAD_REQUEST)

        correct_answers = self.get_answers(serialized_quiz.data["questions"])
        user_answers = self.get_user_answers(answers)
        total_score = self.compute_score(
            correct_answers, user_answers)

        submission_data = {"quiz": quiz_id, "score": total_score}
        submission_serializer = SubmittedAnswerSerializer(data=submission_data)

        if submission_serializer.is_valid():
            saved_submission = submission_serializer.save()

            for answer in answers:
                for ans in answer["answer"]:
                    ans["submission"] = saved_submission.id
                    print(ans)
                    answer_serializer = AnswerSerializer(data=ans)

                    if answer_serializer.is_valid():
                        answer_serializer.save()
                    else:
                        # print(answer_serializer.errors)
                        SubmittedAnswer.objects.get(
                            id=saved_submission.id).delete()
                        return Response(answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # print(submission_serializer.errors)
            return Response(submission_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "data": request.data,
            "score": total_score,
            "isSuccessful": True
        })


class DeleteQuiz(APIView):

    def delete(self, request, id) -> Response:
        try:
            quiz = Quiz.objects.get(id=id).delete()
        except:
            return Response({"error": "Record does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(quiz)
