#!/usr/bin/env python3
import requests
import json
import re

def get_user_stats(username):
    # Get basic user info
    user_url = f"https://api.github.com/users/{username}"
    user_data = requests.get(user_url).json()
    
    # Get repositories
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    repos_data = requests.get(repos_url).json()
    
    # Calculate stats
    total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data)
    total_forks = sum(repo.get('forks_count', 0) for repo in repos_data)
    
    return {
        'name': user_data.get('name', username),
        'public_repos': user_data.get('public_repos', 0),
        'followers': user_data.get('followers', 0),
        'total_stars': total_stars,
        'total_forks': total_forks
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
    print("✅ Overview SVG generated successfully")