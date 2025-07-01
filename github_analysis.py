import requests

def analyze_github_projects(username):
    try:
        response = requests.get(f"https://api.github.com/users/{username}/repos")
        repos = response.json()
        projects = []
        for repo in repos[:3]:  # Limit to top 3
            projects.append({
                "name": repo.get("name"),
                "description": repo.get("description") or "No description",
                "url": repo.get("html_url")
            })
        return projects
    except Exception as e:
        return []
