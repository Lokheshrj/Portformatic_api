from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PortfolioFormSerializer
from .git_utils import create_user_branch  # Git logic with .env support
from django.http import HttpResponse


def home(request):
    return HttpResponse("Backend is working!")


def prepare_user_data(data):
    # Directly map most simple fields
    user_data = {
        "name": data.get("name", ""),
        "phone": data.get("phone", ""),
        "email": data.get("mail", ""),
        "location": data.get("location", ""),
        "address": data.get("address", ""),
        "education": data.get("education", []),  # List of dicts
        "role": data.get("role", ""),
        "description": data.get("description", ""),
        "area_of_interest": data.get("area_of_interest", ""),
        "achievements": data.get("achievements", ""),
        "technical_skill": data.get("technical_skill", ""),
        "soft_skill": data.get("soft_skill", ""),
        "projects": data.get("projects", []),  # List of dicts
        "git_link": data.get("git_link", ""),
        "linkedin": data.get("linkedin", ""),
    }

    # Fix URLs for git_link and linkedin if needed
    if user_data["git_link"] and not user_data["git_link"].startswith("http"):
        user_data["git_link"] = "https://" + user_data["git_link"]
    if user_data["linkedin"] and not user_data["linkedin"].startswith("http"):
        user_data["linkedin"] = "https://" + user_data["linkedin"]

    return user_data


class PortfolioFormView(APIView):
    def post(self, request):
        serializer = PortfolioFormSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            username = data.get("name")
            branch_name = username.replace(" ", "_").lower()
            # or f"user-{username}"
            user_data = prepare_user_data(data)
            print("\n\ndata:\n", user_data)
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
