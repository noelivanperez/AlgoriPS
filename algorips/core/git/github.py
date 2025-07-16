"""Lightweight GitHub API client used for creating and managing pull requests."""

from __future__ import annotations

import requests


class GitHubClient:
    """Minimal GitHub client wrapping a few pull request endpoints."""

    def __init__(self, token: str, base_url: str = "https://api.github.com") -> None:
        self.token = token
        self.base_url = base_url
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
        }

    def create_pull_request(
        self,
        owner: str,
        repo: str,
        head: str,
        base: str,
        title: str,
        body: str | None = None,
        reviewers: list[str] | None = None,
        labels: list[str] | None = None,
    ) -> dict:
        """Create a pull request and return the response JSON."""
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls"
        payload = {"title": title, "head": head, "base": base, "body": body or ""}
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        pr = response.json()

        if reviewers:
            reviews_url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr['number']}/requested_reviewers"
            requests.post(reviews_url, json={"reviewers": reviewers}, headers=self.headers).raise_for_status()
        if labels:
            labels_url = f"{self.base_url}/repos/{owner}/{repo}/issues/{pr['number']}/labels"
            requests.post(labels_url, json={"labels": labels}, headers=self.headers).raise_for_status()
        return pr

    def list_pull_requests(self, owner: str, repo: str, state: str = "open") -> list[dict]:
        """Return pull requests for the repository."""
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls?state={state}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def merge_pull_request(self, owner: str, repo: str, pr_number: int) -> dict:
        """Merge the specified pull request."""
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/merge"
        response = requests.put(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
