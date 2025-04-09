from typing import Any, Dict
import requests
from smolagents.tools import Tool

class GitHubAnalyzerTool(Tool):
    name = "analyze_github_repository"
    description = "Analyzes statistics such as issues, pull_requests, contributors, stars and forks of a public GitHub repository and return a synthesis in markdown string with the results."
    inputs = {
        'github_url': {'type': 'string', 'description': 'The URL of the public GitHub repository to analyze.'}
    }
    output_type = "string"

    def __init__(self, *args, **kwargs):
        self.is_initialized = False

    def forward(self, github_url: str) -> str:
        """
        Analyzes statistics such as issues, pull_requests, contributors, stars and forks of a public GitHub repository and return a synthesis in markdown string with the results.
        Args:
            github_url: The URL of the public GitHub repository to analyze.
        Returns:
            A synthesis of repository statistics in markdown string with the results.
        """
        if not self.validate_github_url(github_url):
            return "Please provide a valid GitHub repository URL."

        user, repo = self.extract_repo_info(github_url)
        api_url = f"https://api.github.com/repos/{user}/{repo}"
        response = requests.get(api_url)

        if response.status_code == 404:
            return "Repository not found."

        data = response.json()

        metrics = {
            "issues": data.get('open_issues_count', 'N/A'),
            "contributors": self.fetch_contributors(github_url),
            "last_commit": self.fetch_last_commit_date(github_url),
            "stars": data.get('stargazers_count', 'N/A'),
            "forks": data.get('forks_count', 'N/A'),
            "pull_requests": self.fetch_pull_requests(github_url)
        }
        markdown_output = "\n".join([
            f"- **{key}**: {value}" for key, value in metrics.items()
        ])

        # Add the repository summary image
        repo_image_url = f"https://github-readme-stats.vercel.app/api/pin/?username={user}&repo={repo}&theme=chartreuse-dark"
        repo_image_markdown = f"![Repo Citation]({repo_image_url})"

        return f"{repo_image_markdown}\n\n{markdown_output}"

    def fetch_contributors(self, github_url: str) -> int:
        """Retrieves the number of contributors for a GitHub repository."""
        user, repo = self.extract_repo_info(github_url)
        api_url = f"https://api.github.com/repos/{user}/{repo}/contributors"
        response = requests.get(api_url)
        if response.status_code != 200:
            return "N/A"
        contributors = response.json()
        return len(contributors)

    def fetch_last_commit_date(self, github_url: str) -> str:
        """Retrieves the date of the last commit for a GitHub repository."""
        user, repo = self.extract_repo_info(github_url)
        api_url = f"https://api.github.com/repos/{user}/{repo}/commits"
        response = requests.get(api_url)
        if response.status_code != 200:
            return "No commits found"
        commits = response.json()
        if commits:
            return commits[0]['commit']['author']['date']
        return "No commits found"

    def fetch_pull_requests(self, github_url: str) -> int:
        """Retrieves the number of open pull requests for a GitHub repository."""
        user, repo = self.extract_repo_info(github_url)
        api_url = f"https://api.github.com/repos/{user}/{repo}/pulls"
        response = requests.get(api_url)
        if response.status_code != 200:
            return "N/A"
        pull_requests = response.json()
        return len(pull_requests)

    def extract_repo_info(self, github_url: str) -> tuple:
        """Extracts repository information from the GitHub URL."""
        parts = github_url.split('/')
        if len(parts) < 5:
            return "URL should be in the format: https://github.com/username/repository"
        return parts[3], parts[4]

    def validate_github_url(self, github_url: str) -> bool:
        """Validates if the provided URL is a valid GitHub repository URL."""
        return "github.com" in github_url
