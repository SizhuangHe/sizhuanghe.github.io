#!/usr/bin/env python3
"""
Update GitHub stars count for projects in _data/projects.yml
"""

import os
import re
import yaml
import requests
from datetime import datetime

def get_github_stars(repo_url, token=None):
    """
    Get star count from GitHub repository
    repo_url: https://github.com/username/repo
    """
    # Extract owner and repo from URL
    match = re.search(r'github\.com/([^/]+)/([^/]+)', repo_url)
    if not match:
        print(f"❌ Invalid GitHub URL: {repo_url}")
        return None

    owner, repo = match.groups()
    # Remove .git suffix if present
    repo = repo.rstrip('.git')

    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'

    try:
        print(f"🔍 Fetching stars for {owner}/{repo}...")
        response = requests.get(api_url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            stars = data.get('stargazers_count', 0)
            print(f"✅ {owner}/{repo}: {stars} stars")
            return stars
        else:
            print(f"⚠️  Failed to fetch {owner}/{repo}: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error fetching {owner}/{repo}: {e}")
        return None

def main():
    print("🚀 Starting GitHub stars update...")

    projects_file = '_data/projects.yml'

    if not os.path.exists(projects_file):
        print(f"❌ File not found: {projects_file}")
        return

    # Load projects.yml
    with open(projects_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if not data or 'projects' not in data:
        print("❌ No projects found in projects.yml")
        return

    # Get GitHub token from environment
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        print("⚠️  No GITHUB_TOKEN found, proceeding without authentication")

    updated = False

    # Update stars for each project
    for project in data['projects']:
        if 'github' not in project:
            continue

        github_url = project['github']
        stars = get_github_stars(github_url, github_token)

        if stars is not None:
            old_stars = project.get('stars', 0)
            project['stars'] = stars

            if old_stars != stars:
                updated = True
                print(f"📊 Updated {project['name']}: {old_stars} → {stars} stars")

    if updated:
        # Save updated data
        with open(projects_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, sort_keys=False, allow_unicode=True, default_flow_style=False)

        print(f"✅ Updated {projects_file}")
        print(f"📅 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("✨ No changes needed")

if __name__ == "__main__":
    main()
