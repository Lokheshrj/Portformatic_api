# views.py
import os
import tempfile
import git
from rest_framework.decorators import api_view
from rest_framework.response import Response


# generator/views.py
from django.http import HttpResponse


def home(request):
    return HttpResponse("Hello from the generator app!")


@api_view(["POST"])
def create_portfolio_branch(request):
    data = request.data
    user_id = data.get("user_id")
    repo_url = "https://github.com/YOUR_USERNAME/YOUR_TEMPLATE_REPO.git"  # Update this

    if not user_id:
        return Response({"error": "user_id is required"}, status=400)

    try:
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = git.Repo.clone_from(repo_url, temp_dir)
            new_branch = f"user-{user_id}"

            # Create new branch
            repo.git.checkout("HEAD", b=new_branch)

            # Commit dummy change to simulate embedding (optional)
            dummy_file = os.path.join(temp_dir, "user_id.txt")
            with open(dummy_file, "w") as f:
                f.write(f"User: {user_id}")

            repo.index.add([dummy_file])
            repo.index.commit(f"Initial commit for {user_id}")
            origin = repo.remote(name="origin")
            origin.push(refspec=f"{new_branch}:{new_branch}")

        return Response(
            {"message": "Branch created successfully", "branch": new_branch}
        )

    except Exception as e:
        return Response({"error": str(e)}, status=500)
