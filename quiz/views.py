# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
#
# from .models import Quiz, Question, Answer
# from .utils import mock_generate_quiz, mock_evaluate_answers
#
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def start_quiz(request):
#     questions_data = mock_generate_quiz()  # Use mock instead of OpenAI API
#
#     quiz = Quiz.objects.create(user=request.user)
#     for idx, question_text in enumerate(questions_data, start=1):
#         Question.objects.create(quiz=quiz, text=question_text, id=idx)
#
#     return Response({'quiz_id': quiz.id, 'questions': questions_data})
#
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def submit_quiz(request):
#     try:
#         quiz_id = request.data.get('quiz_id')
#         answers = request.data.get('answers')
#
#         if not answers:
#             return Response({"error": "No answers provided."}, status=400)
#
#         quiz = Quiz.objects.get(id=quiz_id, user=request.user)
#         results = mock_evaluate_answers(answers)
#
#         for answer_data, result in zip(answers, results):
#             question = Question.objects.get(id=answer_data['question_id'])
#             Answer.objects.create(
#                 question=question,
#                 user_answer=answer_data['user_answer'],
#                 is_correct=result['is_correct']
#             )
#
#         return Response({'results': results}, status=200)
#     except Exception as e:
#         return Response({"error": str(e)}, status=400)

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Category, Question, Answer, QuizAttempt
from .serializers import CategorySerializer, QuestionSerializer, AnswerSerializer, QuizAttemptSerializer
from .chatgpt_service import ChatGPTService


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['post'])
    def generate_question(self, request):
        category_id = request.data.get('category')
        difficulty = request.data.get('difficulty', 'medium')

        print(category_id)
        category = get_object_or_404(Category, id=category_id)
        chatgpt_service = ChatGPTService()

        question_data = chatgpt_service.generate_question(category.name, difficulty)

        if question_data:
            question = Question.objects.create(
                category=category,
                text=question_data['question_text'],
                model_answer=question_data['model_answer'],
                difficulty=difficulty,
                created_by=request.user
            )

            return Response({
                'message': 'Question generated successfully',
                'question': QuestionSerializer(question).data
            })

        return Response({
            'message': 'Failed to generate question'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def submit_answer(self, request, pk=None):
        question = self.get_object()
        answer_text = request.data.get('answer')

        if not answer_text:
            return Response({
                'message': 'Answer text is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        chatgpt_service = ChatGPTService()
        evaluation = chatgpt_service.evaluate_answer(answer_text, question.model_answer)

        if evaluation:
            answer = Answer.objects.create(
                question=question,
                user=request.user,
                text=answer_text,
                score=evaluation['score']
            )

            return Response({
                'message': 'Answer submitted successfully',
                'score': evaluation['score'],
                'feedback': evaluation['feedback']
            })

        return Response({
            'message': 'Failed to evaluate answer'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def generate_quiz(self, request):
        category_id = request.data.get('category_id')
        num_questions = int(request.data.get('num_questions', 5))
        difficulty = request.data.get('difficulty', 'medium')

        category = get_object_or_404(Category, id=category_id)
        chatgpt_service = ChatGPTService()
        generated_questions = []

        for _ in range(num_questions):
            question_data = chatgpt_service.generate_question(category.name, difficulty)
            if question_data:
                question = Question.objects.create(
                    category=category,
                    text=question_data['question_text'],
                    model_answer=question_data['model_answer'],
                    difficulty=difficulty,
                    created_by=request.user
                )
                generated_questions.append(question)

        quiz_attempt = QuizAttempt.objects.create(
            user=request.user,
            category=category,
            total_questions=len(generated_questions),
            score=0
        )

        return Response({
            'quiz_id': quiz_attempt.id,
            'questions': QuestionSerializer(generated_questions, many=True).data
        })


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class QuizAttemptViewSet(viewsets.ModelViewSet):
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizAttemptSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user)
