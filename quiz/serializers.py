from rest_framework import serializers
from .models import Category, Question, Answer, QuizAttempt


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'difficulty', 'category', 'answers']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class QuizAttemptSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = QuizAttempt
        fields = ['id', 'user', 'category', 'category_name', 'username',
                 'score', 'total_questions', 'completed_at']
        read_only_fields = ['user', 'completed_at']