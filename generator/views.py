from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PortfolioFormSerializer
from .git_utils import create_user_branch  # Git logic with .env support
from django.http import HttpResponse


def home(request):
    return HttpResponse("Backend is working!")


def prepare_user_data(data):
    # Parse skills string into list
    skills_raw = data.get("skills", "")
    skills = [skill.strip() for skill in skills_raw.split(",") if skill.strip()]

    # Parse projects string into list of dicts with example description
    projects_raw = data.get("projects", "")
    projects = []
    for proj_name in projects_raw.split(","):
        proj_name = proj_name.strip()
        if proj_name:
            projects.append(
                {
                    "name": f"{proj_name} Project",
                    "description": f"Built a {proj_name.lower()} project.",
                }
            )
    linkedin = data.get("linkedin", "")
    github = data.get("github", "")
    # Fix linkedin and github URLs if needed (optional)
    if linkedin and not linkedin.startswith("http"):
        linkedin = "https://" + linkedin
    if github and not github.startswith("http"):
        github = "https://" + github

    user_data = {
        "name": data.get("full_name", ""),
        "title": data.get("bio", ""),  # Or customize as needed
        "email": data.get("email", ""),
        "about": data.get("bio", ""),
        "skills": skills,
        "projects": projects,
        "linkedin": linkedin,
        "github": github,
    }

    return user_data


class PortfolioFormView(APIView):
    def post(self, request):
        serializer = PortfolioFormSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            username = data.get("username")
            branch_name = username  # or f"user-{username}"

            user_data = prepare_user_data(data)

            try:
                create_user_branch(branch_name, user_data)
            except Exception as e:
                return Response(
                    {"error": f"Branch creation failed: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                {"message": "✅ Form received and branch created!", "data": user_data},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
