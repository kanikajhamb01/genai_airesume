import requests

def analyze_single_repo(repo_url):
    try:
        # Extract owner/repo from URL
        parts = repo_url.rstrip("/").split("/")
        owner = parts[-2]
        repo_name = parts[-1]

        headers = {
            "Accept": "application/vnd.github.mercy-preview+json"  # Enables topics API
        }
        api_url = f"https://api.github.com/repos/{owner}/{repo_name}"
        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            return {"error": f"Could not fetch repo details. Status code: {response.status_code}"}
        repo = response.json()

        # topics require a separate endpoint or preview header (above)
        topics = repo.get("topics", [])
        tech_stack = ", ".join(topics) if topics else repo.get("language", "N/A")

        return {
            "name": repo.get("name"),
            "description": repo.get("description") or "No description",
            "language": repo.get("language") or "N/A",
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "tech_stack": tech_stack
        }
    except Exception as e:
        return {"error": str(e)}
