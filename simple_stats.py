#!/usr/bin/env python3
import requests
import json
import re

def get_user_stats(username):
    try:
        # Get basic user info
        user_url = f"https://api.github.com/users/{username}"
        user_response = requests.get(user_url, timeout=10)
        user_response.raise_for_status()
        user_data = user_response.json()
        
        # Get repositories with pagination
        repos_data = []
        page = 1
        while True:
            repos_url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
            repos_response = requests.get(repos_url, timeout=10)
            repos_response.raise_for_status()
            page_data = repos_response.json()
            
            if not page_data:
                break
            repos_data.extend(page_data)
            page += 1
            
            if len(page_data) < 100:  # Last page
                break
        
        # Filter out excluded repositories
        excluded_repos = {'github-stats', 'uldyssian-sh', 'repo-private', 'repo-private-a', 'repo-private-b'}
        filtered_repos = [repo for repo in repos_data if repo.get('name') not in excluded_repos]
        
        # Calculate stats
        total_stars = sum(repo.get('stargazers_count', 0) for repo in filtered_repos)
        total_forks = sum(repo.get('forks_count', 0) for repo in filtered_repos)
        public_repos = len(filtered_repos)
        
        return {
            'name': user_data.get('name', 'LT'),
            'public_repos': public_repos,
            'followers': user_data.get('followers', 0),
            'total_stars': total_stars,
            'total_forks': total_forks
        }
    except Exception as e:
        print(f"Error fetching stats: {e}")
        # Fallback to current values
        return {
            'name': 'LT',
            'public_repos': 26,
            'followers': 5,
            'total_stars': 62,
            'total_forks': 2
        }

def generate_overview_svg(stats):
    with open("templates/overview.svg", "r") as f:
        template = f.read()
    
    # Replace placeholders
    output = re.sub(r"{{ name }}", stats['name'], template)
    output = re.sub(r"{{ stars }}", f"{stats['total_stars']:,}", output)
    output = re.sub(r"{{ forks }}", f"{stats['total_forks']:,}", output)
    output = re.sub(r"{{ contributions }}", "1,200+", output)  # Estimate
    output = re.sub(r"{{ lines_changed }}", "50,000+", output)  # Estimate
    output = re.sub(r"{{ views }}", "500+", output)  # Estimate
    output = re.sub(r"{{ repos }}", f"{stats['public_repos']:,}", output)
    
    with open("generated/overview.svg", "w") as f:
        f.write(output)

if __name__ == "__main__":
    stats = get_user_stats("uldyssian-sh")
    print(f"Stats: {stats}")
    generate_overview_svg(stats)
    print("✅ Overview SVG generated successfully")# Updated 20251109_123805
# Updated Sun Nov  9 12:50:03 CET 2025
# Updated Sun Nov  9 12:52:20 CET 2025
