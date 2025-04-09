from typing import Any, Dict
import requests

class GitHubCodeQualityTool:
    name = "github_code_quality"
    description = "Analyzes the code quality of a public GitHub repository."
    inputs = {
        'github_url': {'type': 'string', 'description': 'The URL of the public GitHub repository to analyze.'}
    }
    output_type = "dict"

    def __init__(self):
        pass

    def forward(self, github_url: str) -> Dict[str, Any]:
        """
        Analyzes the code quality of a public GitHub repository.

        Args:
            github_url: The URL of the public GitHub repository to analyze.

        Returns:
            A dictionary containing the code quality analysis results.
        """
        metrics = {
            "complexity": "Calculate the average cyclomatic complexity of functions",
            "code_coverage": "Percentage of code covered by tests",
            "issues": self.fetch_open_issues(github_url),
            "contributors": self.fetch_contributors(github_url),
            "last_commit": self.fetch_last_commit_date(github_url),
        }

        return metrics

    def fetch_open_issues(self, github_url: str) -> int:
        """Retrieves the number of open issues for a GitHub repository."""
        api_url = f"https://api.github.com/repos/{self.extract_repo_info(github_url)}/issues"
        response = requests.get(api_url)
        issues = response.json()
        return len(issues)

    def fetch_contributors(self, github_url: str) -> int:
        """Retrieves the number of contributors for a GitHub repository."""
        api_url = f"https://api.github.com/repos/{self.extract_repo_info(github_url)}/contributors"
        response = requests.get(api_url)
        contributors = response.json()
        return len(contributors)

    def fetch_last_commit_date(self, github_url: str) -> str:
        """Retrieves the date of the last commit for a GitHub repository."""
        api_url = f"https://api.github.com/repos/{self.extract_repo_info(github_url)}/commits"
        response = requests.get(api_url)
        commits = response.json()
        if commits:
            return commits[0]['commit']['author']['date']
        return "No commits found"

    def extract_repo_info(self, github_url: str) -> str:
        """Extracts repository information from the GitHub URL."""
        return "/".join(github_url.split("/")[-2:])
