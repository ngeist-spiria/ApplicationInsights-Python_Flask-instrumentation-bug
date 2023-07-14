from django.shortcuts import render
from rest_framework import mixins, viewsets
from core.serializers import PostSerializer

from core.models import Post

# Create your views here.

class PostViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def list(self, request, *args, **kwargs):
        traceparent_header = request.headers.get('traceparent')
        print(traceparent_header)
        return super().list(request, *args, **kwargs)
    