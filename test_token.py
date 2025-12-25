#!/usr/bin/env python3
"""
Test GitHub token functionality
"""

import os
import asyncio
import aiohttp


async def test_github_token():
    """Test GitHub API access with current token"""
    username = os.getenv("GITHUB_ACTOR", "uldyssian-sh")
    access_token = os.getenv("ACCESS_TOKEN") or os.getenv("GITHUB_TOKEN")
    
    print(f"🧪 Testing GitHub API access for {username}")
    print(f"Token available: {'✅ Yes' if access_token else '❌ No'}")
    
    headers = {
        "User-Agent": f"github-stats-test/{username}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    if access_token:
        headers["Authorization"] = f"token {access_token}"
    
    async with aiohttp.ClientSession(headers=headers) as session:
        # Test basic user info
        try:
            async with session.get(f"https://api.github.com/users/{username}") as response:
                print(f"User API: {response.status}")
                if response.status == 200:
                    data = await response.json()
                    print(f"   Name: {data.get('name', 'N/A')}")
                    print(f"   Public repos: {data.get('public_repos', 0)}")
                    print(f"   Followers: {data.get('followers', 0)}")
        except Exception as e:
            print(f"❌ User API error: {e}")
        
        # Test rate limit
        try:
            async with session.get("https://api.github.com/rate_limit") as response:
                print(f"Rate limit API: {response.status}")
                if response.status == 200:
                    data = await response.json()
                    core = data.get('resources', {}).get('core', {})
                    print(f"   Remaining: {core.get('remaining', 0)}/{core.get('limit', 0)}")
        except Exception as e:
            print(f"❌ Rate limit error: {e}")
        
        # Test GraphQL
        if access_token:
            try:
                query = """
                query {
                  viewer {
                    login
                    name
                  }
                }
                """
                async with session.post(
                    "https://api.github.com/graphql",
                    json={"query": query}
                ) as response:
                    print(f"GraphQL API: {response.status}")
                    if response.status == 200:
                        data = await response.json()
                        viewer = data.get('data', {}).get('viewer', {})
                        print(f"   GraphQL login: {viewer.get('login', 'N/A')}")
            except Exception as e:
                print(f"❌ GraphQL error: {e}")


if __name__ == "__main__":
    asyncio.run(test_github_token())