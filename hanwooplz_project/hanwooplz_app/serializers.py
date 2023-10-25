from rest_framework import serializers
from .models import *

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    class Meta:
        model = Comment
        fields = "__all__"