from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'author', 'timestamp']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)  # Nested serializer for related comments

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'timestamp', 'comments']  # Include the 'comments' field

# serializers.py
class PostV2Serializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    word_count = serializers.SerializerMethodField()  # New field

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'timestamp', 'comments', 'word_count']

    def get_word_count(self, obj):
        return len(obj.content.split())  # Calculate word count
