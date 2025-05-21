import os
import tempfile
import shutil
import time
import stat
from git import Repo, GitCommandError
from dotenv import load_dotenv

load_dotenv()


def remove_readonly(func, path, excinfo):
    import errno

    if excinfo[1].errno == errno.EACCES:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        raise


def create_user_branch(branch_name):
    repo_url = os.getenv("REPO_URL")
    github_username = os.getenv("GITHUB_USERNAME")
    github_token = os.getenv("GITHUB_TOKEN")

    if not all([repo_url, github_username, github_token]):
        raise Exception("Missing GitHub credentials or repo URL in .env")

    temp_dir = tempfile.mkdtemp()
    repo = None
    try:
        auth_repo_url = repo_url.replace(
            "https://", f"https://{github_username}:{github_token}@"
        )

        print(f"🔄 Cloning from {repo_url}...")
        repo = Repo.clone_from(auth_repo_url, temp_dir)

        print("✅ Cloned successfully. Checking out 'main' branch...")
        repo.git.checkout("main")

        origin = repo.remote(name="origin")

        # Check if branch exists on remote
        remote_branches = [ref.name.split("/")[-1] for ref in origin.refs]
        if branch_name in remote_branches:
            print(
                f"♻️ Branch '{branch_name}' exists on remote. Checking out and resetting local branch..."
            )
            if branch_name in repo.heads:
                repo.delete_head(branch_name, force=True)  # Delete local if exists

            repo.git.checkout(f"origin/{branch_name}", b=branch_name)
            # Reset local branch hard to remote
            repo.git.reset("--hard", f"origin/{branch_name}")
        else:
            print(f"🔧 Creating new branch '{branch_name}' from main...")
            if branch_name in repo.heads:
                repo.delete_head(branch_name, force=True)
            repo.git.checkout("-b", branch_name)

        dummy_file_path = os.path.join(temp_dir, "README.md")
        with open(dummy_file_path, "a") as f:
            f.write(f"\nPortfolio for {branch_name}\n")

        repo.index.add(["README.md"])
        repo.index.commit(f"📝 Updated portfolio branch for {branch_name}")

        print("🚀 Pushing branch to origin...")
        push_info = origin.push(refspec=f"{branch_name}:{branch_name}")

        for info in push_info:
            print(f"Push status summary: {info.summary}")
            if info.flags & info.ERROR:
                raise Exception(f"Push failed with error: {info.summary}")

        print("✅ Branch pushed successfully.")

    except GitCommandError as e:
        raise Exception(f"Git command failed: {e}")
    finally:
        print("Waiting 2 seconds before cleanup to release file locks...")
        time.sleep(2)

        if repo:
            try:
                repo.close()
            except Exception:
                pass

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, onerror=remove_readonly)
            print("🧹 Cleaned up temporary directory.")
