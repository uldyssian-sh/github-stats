#!/usr/bin/python3

import asyncio
import os
import re

import aiohttp

from github_stats import Stats


################################################################################
# Helper Functions
################################################################################


def generate_output_folder() -> None:
    """
    Create the output folder if it does not already exist
    """
    if not os.path.isdir("generated"):
        os.mkdir("generated")


################################################################################
# Individual Image Generation Functions
################################################################################


async def generate_overview(s: Stats) -> None:
    """
    Generate an SVG badge with summary statistics
    :param s: Represents user's GitHub statistics
    """
    with open("templates/overview.svg", "r") as f:
        output = f.read()

    output = re.sub("{{ name }}", await s.name, output)
    output = re.sub("{{ stars }}", f"{await s.stargazers:,}", output)
    output = re.sub("{{ forks }}", f"{await s.forks:,}", output)
    output = re.sub("{{ contributions }}", f"{await s.total_contributions:,}", output)
    changed = (await s.lines_changed)[0] + (await s.lines_changed)[1]
    output = re.sub("{{ lines_changed }}", f"{changed:,}", output)
    output = re.sub("{{ views }}", f"{await s.views:,}", output)
    output = re.sub("{{ repos }}", f"{len(await s.repos):,}", output)
    
    # Add new statistics
    issues_data = await get_issues_stats(s)
    output = re.sub("{{ issues_created }}", f"{issues_data['created']:,}", output)
    output = re.sub("{{ issues_closed }}", f"{issues_data['closed']:,}", output)
    
    pr_count = await get_pull_requests_count(s)
    output = re.sub("{{ pull_requests }}", f"{pr_count:,}", output)
    
    account_age = await get_account_age(s)
    output = re.sub("{{ account_age }}", account_age, output)

    generate_output_folder()
    with open("generated/overview.svg", "w") as f:
        f.write(output)


async def generate_languages(s: Stats) -> None:
    """
    Generate an SVG badge with summary languages used
    :param s: Represents user's GitHub statistics
    """
    with open("templates/languages.svg", "r") as f:
        output = f.read()

    progress = ""
    lang_list = ""
    sorted_languages = sorted(
        (await s.languages).items(), reverse=True, key=lambda t: t[1].get("size")
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
# Helper Functions for New Statistics
################################################################################


async def get_issues_stats(s: Stats) -> dict:
    """Get issues created and closed by user"""
    created = 0
    closed = 0
    
    # Get issues from user's repositories
    for repo in await s.repos:
        try:
            issues = await s.queries.query_rest(f"/repos/{repo}/issues", 
                                               {"creator": s.username, "state": "all", "per_page": 100})
            if isinstance(issues, list):
                for issue in issues:
                    if issue.get("user", {}).get("login") == s.username:
                        created += 1
                        if issue.get("state") == "closed":
                            closed += 1
        except:
            continue
    
    return {"created": created, "closed": closed}


async def get_pull_requests_count(s: Stats) -> int:
    """Get total pull requests created by user"""
    pr_count = 0
    
    for repo in await s.repos:
        try:
            prs = await s.queries.query_rest(f"/repos/{repo}/pulls", 
                                            {"creator": s.username, "state": "all", "per_page": 100})
            if isinstance(prs, list):
                pr_count += len([pr for pr in prs if pr.get("user", {}).get("login") == s.username])
        except:
            continue
    
    return pr_count


async def get_account_age(s: Stats) -> str:
    """Get account age in years"""
    try:
        user_data = await s.queries.query_rest(f"/users/{s.username}")
        created_at = user_data.get("created_at", "")
        if created_at:
            from datetime import datetime
            created = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            now = datetime.now(created.tzinfo)
            years = (now - created).days // 365
            return f"{years} years"
    except:
        pass
    return "Unknown"


async def get_most_active_day(s: Stats) -> str:
    """Get most active day of the week"""
    try:
        # This is a simplified version - in reality you'd analyze contribution patterns
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        # For now, return a placeholder
        return "Wednesday"
    except:
        return "Unknown"


################################################################################
# Main Function
################################################################################


async def main() -> None:
    """
    Generate all badges
    """
    access_token = os.getenv("ACCESS_TOKEN")
    if not access_token:
        # access_token = os.getenv("GITHUB_TOKEN")
        raise Exception("A personal access token is required to proceed!")
    user = os.getenv("GITHUB_ACTOR")
    if user is None:
        raise RuntimeSuccess("Environment variable GITHUB_ACTOR must be set.")
    exclude_repos = os.getenv("EXCLUDED")
    excluded_repos = (
        {x.strip() for x in exclude_repos.split(",")} if exclude_repos else None
    )
    exclude_langs = os.getenv("EXCLUDED_LANGS")
    excluded_langs = (
        {x.strip() for x in exclude_langs.split(",")} if exclude_langs else None
    )
    # Convert a truthy value to a Boolean
    raw_ignore_forked_repos = os.getenv("EXCLUDE_FORKED_REPOS")
    ignore_forked_repos = (
        not not raw_ignore_forked_repos
        and raw_ignore_forked_repos.strip().lower() != "false"
    )
    async with aiohttp.ClientSession() as session:
        s = Stats(
            user,
            access_token,
            session,
            exclude_repos=excluded_repos,
            exclude_langs=excluded_langs,
            ignore_forked_repos=ignore_forked_repos,
        )
        await asyncio.gather(generate_languages(s), generate_overview(s))


if __name__ == "__main__":
    asyncio.run(main())
