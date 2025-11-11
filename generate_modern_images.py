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
# Modern Image Generation Functions
################################################################################


async def generate_modern_overview(s: Stats) -> None:
    """
    Generate a modern SVG badge with summary statistics
    :param s: Represents user's GitHub statistics
    """
    with open("templates/modern-overview.svg", "r") as f:
        output = f.read()

    output = re.sub("{{ name }}", await s.name, output)
    output = re.sub("{{ stars }}", f"{await s.stargazers:,}", output)
    output = re.sub("{{ forks }}", f"{await s.forks:,}", output)
    output = re.sub("{{ contributions }}", f"{await s.total_contributions:,}", output)
    changed = (await s.lines_changed)[0] + (await s.lines_changed)[1]
    output = re.sub("{{ lines_changed }}", f"{changed:,}", output)
    output = re.sub("{{ views }}", f"{await s.views:,}", output)
    output = re.sub("{{ repos }}", f"{len(await s.repos):,}", output)

    generate_output_folder()
    with open("generated/modern-overview.svg", "w") as f:
        f.write(output)


async def generate_modern_languages(s: Stats) -> None:
    """
    Generate a modern SVG badge with summary languages used
    :param s: Represents user's GitHub statistics
    """
    with open("templates/modern-languages.svg", "r") as f:
        output = f.read()

    progress = ""
    lang_list = ""
    sorted_languages = sorted(
        (await s.languages).items(), reverse=True, key=lambda t: t[1].get("size")
    )
    
    # Take only top 8 languages for better display
    top_languages = sorted_languages[:8]
    
    for i, (lang, data) in enumerate(top_languages):
        color = data.get("color")
        color = color if color is not None else "#6e7681"
        
        # Progress bar
        progress += (
            f'<span style="background-color: {color};'
            f'width: {data.get("prop", 0):0.3f}%;" '
            f'class="progress-item"></span>'
        )
        
        # Language list items
        lang_list += f"""
<div class="lang-item">
  <div class="lang-dot" style="background-color: {color};"></div>
  <span class="lang-name">{lang}</span>
  <span class="lang-percent">{data.get("prop", 0):0.1f}%</span>
</div>
"""

    output = re.sub(r"{{ progress }}", progress, output)
    output = re.sub(r"{{ lang_list }}", lang_list, output)

    generate_output_folder()
    with open("generated/modern-languages.svg", "w") as f:
        f.write(output)


################################################################################
# Main Function
################################################################################


async def main() -> None:
    """
    Generate all modern badges
    """
    access_token = os.getenv("ACCESS_TOKEN")
    if not access_token:
        access_token = os.getenv("GITHUB_TOKEN")
        if not access_token:
            raise Exception("A personal access token is required to proceed!")
    
    user = os.getenv("GITHUB_ACTOR")
    if user is None:
        raise Exception("Environment variable GITHUB_ACTOR must be set.")
    
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
        await asyncio.gather(generate_modern_languages(s), generate_modern_overview(s))


if __name__ == "__main__":
    asyncio.run(main())