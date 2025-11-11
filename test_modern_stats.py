#!/usr/bin/env python3
"""
Test script for modern GitHub stats generation
"""

import os
import asyncio
from generate_modern_images import main

async def test_generation():
    """Test the modern stats generation"""
    
    # Set test environment variables
    os.environ["GITHUB_ACTOR"] = "uldyssian-sh"
    
    # You'll need to set your GitHub token
    if not os.getenv("ACCESS_TOKEN") and not os.getenv("GITHUB_TOKEN"):
        print("⚠️  Please set ACCESS_TOKEN or GITHUB_TOKEN environment variable")
        print("   You can create a personal access token at:")
        print("   https://github.com/settings/tokens")
        return
    
    try:
        print("🚀 Generating modern GitHub stats...")
        await main()
        print("✅ Modern stats generated successfully!")
        print("📁 Check the generated/ folder for:")
        print("   - modern-overview.svg")
        print("   - modern-languages.svg")
        
    except Exception as e:
        print(f"❌ Error generating stats: {e}")

if __name__ == "__main__":
    asyncio.run(test_generation())