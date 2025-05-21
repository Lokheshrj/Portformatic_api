from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PortfolioFormSerializer
from .git_utils import create_user_branch  # Git logic with .env support
from django.http import HttpResponse


def home(request):
    return HttpResponse("Backend is working!")


class PortfolioFormView(APIView):
    def post(self, request):
        print("📥 Incoming POST data:", request.data)  # For debugging

        serializer = PortfolioFormSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            username = data.get("username")
            branch_name = username  # Or use f"user-{username}" for uniqueness

            try:
                create_user_branch(branch_name)
            except Exception as e:
                print(f"❌ Git Error: {str(e)}")  # Log backend error
                return Response(
                    {"error": f"Branch creation failed: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                {"message": "✅ Form received and branch created!", "data": data},
                status=status.HTTP_201_CREATED,
            )

        print("❌ Serializer Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
