from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListQuizzes.as_view()),
    path('quiz/create/', views.CreateQuiz.as_view()),
    path('quiz/<int:id>', views.GetQuiz.as_view()),
    path('quiz/<int:id>/delete', views.DeleteQuiz.as_view()),
    path('quiz/evaluate/', views.EvaluateQuiz.as_view())
]
