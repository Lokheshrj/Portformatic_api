from rest_framework import serializers


class EducationSerializer(serializers.Serializer):
    type = serializers.CharField(allow_blank=True)
    start = serializers.CharField(allow_blank=True)
    end = serializers.CharField(allow_blank=True)
    course = serializers.CharField(allow_blank=True)
    field_of_study = serializers.CharField(allow_blank=True)
    institution = serializers.CharField(allow_blank=True)
    marks = serializers.CharField(allow_blank=True)


class ProjectSerializer(serializers.Serializer):
    title = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)
    git_link = serializers.URLField(allow_blank=True, required=False)
    tech_stack = serializers.CharField(allow_blank=True)


class PortfolioFormSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20, allow_blank=True, required=False)
    mail = serializers.EmailField()  # matches JSON 'mail'
    location = serializers.CharField(allow_blank=True, required=False)
    address = serializers.CharField(allow_blank=True, required=False)
    education = EducationSerializer(many=True, required=False)
    role = serializers.CharField(allow_blank=True, required=False)
    description = serializers.CharField(allow_blank=True, required=False)
    area_of_interest = serializers.CharField(allow_blank=True, required=False)
    achievements = serializers.CharField(allow_blank=True, required=False)
    technical_skill = serializers.CharField(allow_blank=True, required=False)
    soft_skill = serializers.CharField(allow_blank=True, required=False)
    projects = ProjectSerializer(many=True, required=False)
    git_link = serializers.URLField(allow_blank=True, required=False)
    linkedin = serializers.URLField(allow_blank=True, required=False)
