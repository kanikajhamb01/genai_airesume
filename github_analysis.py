from main import analyze_github_repo_with_ai
from github import Github

def analyze_github_repo(repo_url):
    try:
        g = Github()  # anonymous access
        repo = g.get_repo(repo_url.split("github.com/")[1])
        readme = repo.get_readme().decoded_content.decode()
        return analyze_github_repo_with_ai(readme, repo.name)
    except Exception as e:
        return "GitHub analysis failed: " + str(e)
