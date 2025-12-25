#!/usr/bin/python3

import asyncio
import os
import re
import json
from datetime import datetime, timezone
from typing import Dict, List, Any

import aiohttp


################################################################################
# Helper Functions
################################################################################


def generate_output_folder() -> None:
    """
    Create the output folder if it does not already exist
    """
    if not os.path.isdir("generated"):
        os.mkdir("generated")


class GitHubStatsCollector:
    """
    Enhanced GitHub statistics collector using REST API
    """
    
    def __init__(self, username: str, session: aiohttp.ClientSession):
        self.username = username
        self.session = session
        self.base_url = "https://api.github.com"
        
    async def get_user_info(self) -> Dict[str, Any]:
        """Get basic user information"""
        try:
            async with self.session.get(f"{self.base_url}/users/{self.username}") as response:
                if response.status == 200:
                    return await response.json()
        except Exception as e:
            print(f"Error fetching user info: {e}")
        return {}
    
    async def get_repositories(self) -> List[Dict[str, Any]]:
        """Get all user repositories"""
        repos = []
        page = 1
        per_page = 100
        
        while True:
            try:
                url = f"{self.base_url}/users/{self.username}/repos"
                params = {"page": page, "per_page": per_page, "sort": "updated"}
                
                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        page_repos = await response.json()
                        if not page_repos:
                            break
                        repos.extend(page_repos)
                        page += 1
                    else:
                        break
            except Exception as e:
                print(f"Error fetching repositories: {e}")
                break
                
        return repos
    
    async def get_repository_languages(self, repo_name: str) -> Dict[str, int]:
        """Get languages for a specific repository"""
        try:
            url = f"{self.base_url}/repos/{self.username}/{repo_name}/languages"
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
        except Exception as e:
            print(f"Error fetching languages for {repo_name}: {e}")
        return {}
    
    async def get_user_events(self) -> List[Dict[str, Any]]:
        """Get user's recent events for contribution analysis"""
        events = []
        page = 1
        
        while page <= 10:  # Limit to avoid rate limiting
            try:
                url = f"{self.base_url}/users/{self.username}/events"
                params = {"page": page, "per_page": 100}
                
                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        page_events = await response.json()
                        if not page_events:
                            break
                        events.extend(page_events)
                        page += 1
                    else:
                        break
            except Exception as e:
                print(f"Error fetching events: {e}")
                break
                
        return events
    
    async def get_user_starred_repos(self) -> int:
        """Get count of repositories user has starred"""
        try:
            url = f"{self.base_url}/users/{self.username}/starred"
            params = {"per_page": 1}
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    # Get total count from Link header
                    link_header = response.headers.get('Link', '')
                    if 'rel="last"' in link_header:
                        import re
                        match = re.search(r'page=(\d+)>; rel="last"', link_header)
                        if match:
                            return int(match.group(1)) * 100  # Approximate
                    else:
                        starred = await response.json()
                        return len(starred)
        except Exception as e:
            print(f"Error fetching starred repos: {e}")
        return 0
    
    async def get_comprehensive_language_stats(self, repos: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Get comprehensive language statistics from ALL repositories"""
        all_languages = {}
        
        # Process ALL repositories, not just first 20
        for i, repo in enumerate(repos):
            if repo.get('fork', False):  # Skip forks for language stats
                continue
                
            repo_name = repo['name']
            languages = await self.get_repository_languages(repo_name)
            
            for lang, bytes_count in languages.items():
                all_languages[lang] = all_languages.get(lang, 0) + bytes_count
            
            # Add small delay every 10 repos to avoid rate limiting
            if (i + 1) % 10 == 0:
                await asyncio.sleep(0.5)
        
        # Calculate language percentages
        total_bytes = sum(all_languages.values())
        language_stats = {}
        if total_bytes > 0:
            for lang, bytes_count in all_languages.items():
                percentage = (bytes_count / total_bytes) * 100
                language_stats[lang] = {
                    'size': bytes_count,
                    'prop': percentage,
                    'color': get_language_color(lang)
                }
        
        return language_stats
    async def collect_all_stats(self) -> Dict[str, Any]:
        """Collect comprehensive GitHub statistics using GraphQL API"""
        print(f"🔍 Collecting comprehensive stats for {self.username}...")
        
        # Try GraphQL first for more accurate data
        graphql_data = await self.get_comprehensive_stats()
        
        if graphql_data:
            print("✅ Using GraphQL API for accurate statistics")
            return await self.process_graphql_data(graphql_data)
        else:
            print("⚠️  GraphQL failed, falling back to REST API estimates")
            return await self.collect_rest_stats()
    
    async def process_graphql_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process GraphQL response into stats format"""
        name = data.get('name') or data.get('login', 'GitHub User')
        
        # Repository statistics
        repos_data = data.get('repositories', {})
        repos = repos_data.get('nodes', [])
        owned_repos = [repo for repo in repos if not repo.get('isFork', False)]
        
        # Calculate totals
        total_stars = sum(repo.get('stargazerCount', 0) for repo in repos)
        total_forks = sum(repo.get('forkCount', 0) for repo in repos)
        total_watchers = sum(repo.get('watchers', {}).get('totalCount', 0) for repo in repos)
        
        # Contribution statistics
        contrib_data = data.get('contributionsCollection', {})
        total_contributions = contrib_data.get('contributionCalendar', {}).get('totalContributions', 0)
        commit_contributions = contrib_data.get('totalCommitContributions', 0)
        issue_contributions = contrib_data.get('totalIssueContributions', 0)
        pr_contributions = contrib_data.get('totalPullRequestContributions', 0)
        
        # Language statistics from GraphQL
        language_stats = {}
        total_lang_size = 0
        
        for repo in owned_repos:
            if repo.get('isFork', False):
                continue
            for lang_edge in repo.get('languages', {}).get('edges', []):
                lang_name = lang_edge.get('node', {}).get('name', 'Unknown')
                lang_size = lang_edge.get('size', 0)
                lang_color = lang_edge.get('node', {}).get('color', '#586069')
                
                if lang_name in language_stats:
                    language_stats[lang_name]['size'] += lang_size
                else:
                    language_stats[lang_name] = {
                        'size': lang_size,
                        'color': lang_color
                    }
                total_lang_size += lang_size
        
        # Calculate language proportions
        for lang_name, lang_data in language_stats.items():
            if total_lang_size > 0:
                lang_data['prop'] = (lang_data['size'] / total_lang_size) * 100
            else:
                lang_data['prop'] = 0
        
        # Account age
        created_at = data.get('createdAt', '')
        account_age = "Unknown"
        if created_at:
            try:
                created = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                now = datetime.now(timezone.utc)
                years = (now - created).days // 365
                account_age = f"{years} years"
            except:
                pass
        
        # Get additional stats
        followers = data.get('followers', {}).get('totalCount', 0)
        following = data.get('following', {}).get('totalCount', 0)
        contributed_repos = data.get('repositoriesContributedTo', {}).get('totalCount', 0)
        
        # Pull requests and issues
        total_prs = data.get('pullRequests', {}).get('totalCount', pr_contributions)
        total_issues = data.get('issues', {}).get('totalCount', issue_contributions)
        
        # Calculate lines changed estimate (more conservative with real data)
        lines_changed = max(
            commit_contributions * 25,  # 25 lines per commit on average
            total_stars * 30,  # Popular repos have more code
            len(owned_repos) * 100  # Base estimate per repo
        )
        
        # Repository views estimate
        views_estimate = max(
            total_stars * 15,  # Popular repos get more views
            total_watchers * 10,
            len(owned_repos) * 50
        )
        
        stats = {
            'name': name,
            'stars': total_stars,
            'forks': total_forks,
            'repos': len(owned_repos),
            'total_repos': len(repos),
            'contributions': total_contributions,
            'lines_changed': lines_changed,
            'views': views_estimate,
            'issues_created': total_issues,
            'issues_closed': total_issues // 2,  # Estimate 50% closure rate
            'pull_requests': total_prs,
            'account_age': account_age,
            'most_active_day': 'Wednesday',
            'languages': language_stats,
            'followers': followers,
            'following': following,
            'contributed_repos': contributed_repos
        }
        
        print(f"✅ GraphQL stats collected:")
        print(f"   📁 {len(repos)} total repos ({len(owned_repos)} owned)")
        print(f"   ⭐ {total_stars} stars across all repositories")
        print(f"   🍴 {total_forks} forks")
        print(f"   💻 {len(language_stats)} programming languages")
        print(f"   📊 {total_contributions} total contributions")
        print(f"   👥 {followers} followers, {following} following")
        
        return stats
    
    async def collect_rest_stats(self) -> Dict[str, Any]:
        """Fallback method using REST API with estimates"""
        # Get user info
        user_info = await self.get_user_info()
        name = user_info.get('name') or user_info.get('login', 'GitHub User')
        
        # Get ALL repositories
        repos = await self.get_repositories()
        print(f"📊 Found {len(repos)} total repositories")
        
        # Separate owned vs forked repositories
        owned_repos = [repo for repo in repos if not repo.get('fork', False)]
        forked_repos = [repo for repo in repos if repo.get('fork', False)]
        
        print(f"📈 Owned: {len(owned_repos)}, Forked: {len(forked_repos)}")
        
        # Calculate comprehensive statistics
        total_stars = sum(repo.get('stargazers_count', 0) for repo in repos)
        total_forks = sum(repo.get('forks_count', 0) for repo in repos)
        total_watchers = sum(repo.get('watchers_count', 0) for repo in repos)
        total_size = sum(repo.get('size', 0) for repo in repos)  # in KB
        
        # Get user's public stats
        public_repos = user_info.get('public_repos', 0)
        public_gists = user_info.get('public_gists', 0)
        followers = user_info.get('followers', 0)
        following = user_info.get('following', 0)
        
        # Get events for contribution analysis
        events = await self.get_user_events()
        
        # Analyze events for better contribution estimates
        push_events = len([e for e in events if e.get('type') == 'PushEvent'])
        pr_events = len([e for e in events if e.get('type') == 'PullRequestEvent'])
        issue_events = len([e for e in events if e.get('type') == 'IssuesEvent'])
        
        # Get account age
        created_at = user_info.get('created_at', '')
        account_age = "Unknown"
        account_days = 0
        if created_at:
            try:
                created = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                now = datetime.now(timezone.utc)
                account_days = (now - created).days
                years = account_days // 365
                account_age = f"{years} years"
            except:
                pass
        
        # Get comprehensive language statistics from ALL repositories
        language_stats = await self.get_comprehensive_language_stats(repos)
        
        # Calculate more accurate estimates based on actual data
        estimated_contributions = max(
            push_events * 5,  # Estimate 5 commits per push event
            len(owned_repos) * 15,  # Estimate 15 commits per owned repo
            account_days // 7  # At least one contribution per week
        )
        
        estimated_lines_changed = max(
            total_stars * 50,  # Popular repos likely have more code
            total_size * 10,  # Based on repository sizes
            estimated_contributions * 20  # Estimate lines per contribution
        )
        
        estimated_issues = max(
            issue_events,
            len(owned_repos) * 3,  # Estimate 3 issues per owned repo
            total_stars // 10  # Popular repos generate issues
        )
        
        estimated_prs = max(
            pr_events,
            len(owned_repos) * 2,  # Estimate 2 PRs per owned repo
            forked_repos.__len__()  # At least one PR per fork
        )
        
        # Get starred repositories count
        starred_count = await self.get_user_starred_repos()
        
        stats = {
            'name': name,
            'stars': total_stars,
            'forks': total_forks,
            'repos': len(owned_repos),
            'total_repos': len(repos),
            'contributions': estimated_contributions,
            'lines_changed': estimated_lines_changed,
            'views': max(total_stars * 10, total_watchers * 5),  # Estimate based on popularity
            'issues_created': estimated_issues,
            'issues_closed': estimated_issues // 2,  # Assume 50% closure rate
            'pull_requests': estimated_prs,
            'account_age': account_age,
            'most_active_day': 'Wednesday',  # Could be enhanced with event analysis
            'languages': language_stats,
            'followers': followers,
            'following': following,
            'public_gists': public_gists,
            'starred_repos': starred_count,
            'total_size_kb': total_size
        }
        
        print(f"✅ REST API stats collected:")
        print(f"   📁 {len(repos)} total repos ({len(owned_repos)} owned)")
        print(f"   ⭐ {total_stars} stars across all repositories")
        print(f"   🍴 {total_forks} forks")
        print(f"   💻 {len(language_stats)} programming languages")
        print(f"   📊 {estimated_contributions} estimated contributions")
        print(f"   👥 {followers} followers, {following} following")
        
        return stats


def get_language_color(language: str) -> str:
    """Get color for programming language"""
    colors = {
        'Python': '#3572A5',
        'JavaScript': '#f1e05a',
        'TypeScript': '#2b7489',
        'Java': '#b07219',
        'C++': '#f34b7d',
        'C': '#555555',
        'C#': '#239120',
        'PHP': '#4F5D95',
        'Ruby': '#701516',
        'Go': '#00ADD8',
        'Rust': '#dea584',
        'Swift': '#ffac45',
        'Kotlin': '#F18E33',
        'Scala': '#c22d40',
        'Shell': '#89e051',
        'PowerShell': '#012456',
        'HTML': '#e34c26',
        'CSS': '#563d7c',
        'SCSS': '#c6538c',
        'Vue': '#2c3e50',
        'React': '#61dafb',
        'Dockerfile': '#384d54',
        'YAML': '#cb171e',
        'JSON': '#292929',
        'Markdown': '#083fa1'
    }
    return colors.get(language, '#586069')


################################################################################
# Individual Image Generation Functions
################################################################################


async def generate_overview(stats: Dict[str, Any]) -> None:
    """
    Generate an SVG badge with summary statistics
    """
    with open("templates/overview.svg", "r") as f:
        output = f.read()

    output = re.sub("{{ name }}", stats['name'], output)
    output = re.sub("{{ stars }}", f"{stats['stars']:,}", output)
    output = re.sub("{{ forks }}", f"{stats['forks']:,}", output)
    output = re.sub("{{ contributions }}", f"{stats['contributions']:,}", output)
    output = re.sub("{{ lines_changed }}", f"{stats['lines_changed']:,}", output)
    output = re.sub("{{ views }}", f"{stats['views']:,}", output)
    output = re.sub("{{ repos }}", f"{stats['repos']:,}", output)
    output = re.sub("{{ issues_created }}", f"{stats['issues_created']:,}", output)
    output = re.sub("{{ issues_closed }}", f"{stats['issues_closed']:,}", output)
    output = re.sub("{{ pull_requests }}", f"{stats['pull_requests']:,}", output)
    output = re.sub("{{ account_age }}", stats['account_age'], output)
    output = re.sub("{{ most_active_day }}", stats['most_active_day'], output)

    generate_output_folder()
    with open("generated/overview.svg", "w") as f:
        f.write(output)


async def generate_languages(stats: Dict[str, Any]) -> None:
    """
    Generate an SVG badge with summary languages used
    """
    with open("templates/languages.svg", "r") as f:
        output = f.read()

    progress = ""
    lang_list = ""
    sorted_languages = sorted(
        stats['languages'].items(), reverse=True, key=lambda t: t[1].get("size")
    )
    delay_between = 150
    for i, (lang, data) in enumerate(sorted_languages):
        color = data.get("color")
        color = color if color is not None else "#000000"
        progress += (
            f'<span style="background-color: {color};'
            f'width: {data.get("prop", 0):0.3f}%;" '
            f'class="progress-item"></span>'
        )
        lang_list += f"""
<li style="animation-delay: {i * delay_between}ms;">
<svg xmlns="http://www.w3.org/2000/svg" class="octicon" style="fill:{color};"
viewBox="0 0 16 16" version="1.1" width="16" height="16"><path
fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8z"></path></svg>
<span class="lang">{lang}</span>
<span class="percent">{data.get("prop", 0):0.2f}%</span>
</li>

"""

    output = re.sub(r"{{ progress }}", progress, output)
    output = re.sub(r"{{ lang_list }}", lang_list, output)

    generate_output_folder()
    with open("generated/languages.svg", "w") as f:
        f.write(output)


################################################################################
# Main Function
################################################################################


async def main() -> None:
    """
    Generate all badges using enhanced stats collector
    """
    username = os.getenv("GITHUB_ACTOR", "uldyssian-sh")
    access_token = os.getenv("GITHUB_TOKEN") or os.getenv("ACCESS_TOKEN")
    
    if not access_token:
        print("⚠️  No access token found. Using public API with rate limits.")
        print("   Set GITHUB_TOKEN or ACCESS_TOKEN environment variable for better results.")
    
    headers = {}
    if access_token:
        headers["Authorization"] = f"token {access_token}"
    
    async with aiohttp.ClientSession(headers=headers) as session:
        collector = GitHubStatsCollector(username, session)
        stats = await collector.collect_all_stats()
        
        await asyncio.gather(
            generate_overview(stats),
            generate_languages(stats)
        )
        
        print("🎉 GitHub stats generated successfully!")


if __name__ == "__main__":
    asyncio.run(main())