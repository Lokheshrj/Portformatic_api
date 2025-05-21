from rest_framework import serializers


class PortfolioFormSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    bio = serializers.CharField(allow_blank=True)
    skills = serializers.CharField(allow_blank=True)
    projects = serializers.CharField(allow_blank=True)
    linkedin = serializers.URLField(allow_blank=True, required=False)
    github = serializers.URLField(allow_blank=True, required=False)
    template_choice = serializers.CharField(max_length=50)
