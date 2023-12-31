from rest_framework import serializers

from core.models import Post

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'text',
            'created_at',
            'updated_at'
        )
        read_only_fields = (
            'created_at', 'updated_at'
        )