from .models import *
from rest_framework import serializers
from user.models import User
from user.serializers import *
import json
from rest_framework.exceptions import ValidationError

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        
class PostListSerializer(serializers.ModelSerializer):
    owner = UserListSerializer()
    created_time = serializers.SerializerMethodField('convert_date')

    class Meta:
        model = Post
        fields = "__all__"
    
    def convert_date(self, obj):
        return obj.created_time
