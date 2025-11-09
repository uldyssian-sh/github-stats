# GitHub Stats Generator

[![CI](https://github.com/uldyssian-sh/github-stats/actions/workflows/ci.yml/badge.svg)](https://github.com/uldyssian-sh/github-stats/actions/workflows/ci.yml)
[![Security](https://github.com/uldyssian-sh/github-stats/actions/workflows/security.yml/badge.svg)](https://github.com/uldyssian-sh/github-stats/actions/workflows/security.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## Overview

GitHub repository analytics and statistics generator with automated workflows.

**Technology Stack:** Python 3.9+, GitHub GraphQL API v4, GitHub REST API v3, aiohttp, asyncio

## Features

- 📊 **Real-time Analytics** - Live GitHub repository statistics
- 📈 **Visual Reports** - SVG-based statistics visualization
- 🔄 **Automated Generation** - GitHub Actions integration
- 🌐 **Free Tier Optimized** - Designed for GitHub Free tier limits

## Generated Statistics

### Overview Statistics
![GitHub Stats Overview](./generated/overview.svg)

### Language Distribution
![GitHub Languages](./generated/languages.svg)

## Quick Start

```bash
# Clone repository
git clone https://github.com/uldyssian-sh/github-stats.git
cd github-stats

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export ACCESS_TOKEN="your_github_token"
export GITHUB_ACTOR="your_username"

# Generate statistics
python generate_images.py
```

## Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `ACCESS_TOKEN` | GitHub Personal Access Token | ✅ |
| `GITHUB_ACTOR` | GitHub username | ✅ |
| `EXCLUDED` | Repos to exclude | ❌ |
| `EXCLUDED_LANGS` | Languages to exclude | ❌ |

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

### Contributors
- **dependabot[bot]** - Automated dependency updates
- **actions-user** - GitHub Actions automation  
- **uldyssian-sh LT** - Primary maintainer

## License

MIT License - see [LICENSE](LICENSE) file.

## Links

- [Repository](https://github.com/uldyssian-sh/github-stats)
- [Issues](https://github.com/uldyssian-sh/github-stats/issues)
- [Actions](https://github.com/uldyssian-sh/github-stats/actions)# Stats update trigger Sun Oct 12 18:57:12 CEST 2025
# Test verification Sat Nov  1 15:12:20 CET 2025

## Recent Updates
- Enhanced statistics collection
- Improved visualization capabilities
- Better performance monitoring
# Updated 20251109_123805
# Updated Sun Nov  9 12:50:03 CET 2025
# Updated Sun Nov  9 12:52:20 CET 2025
