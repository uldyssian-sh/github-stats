# GitHub Stats Generator

[![Enterprise CI/CD Pipeline](https://github.com/uldyssian-sh/github-stats/actions/workflows/ci.yml/badge.svg)](https://github.com/uldyssian-sh/github-stats/actions/workflows/ci.yml)
[![Security Audit](https://github.com/uldyssian-sh/github-stats/actions/workflows/security.yml/badge.svg)](https://github.com/uldyssian-sh/github-stats/actions/workflows/security.yml)
[![GitHub Stats Generator](https://github.com/uldyssian-sh/github-stats/actions/workflows/stats-generator.yml/badge.svg)](https://github.com/uldyssian-sh/github-stats/actions/workflows/stats-generator.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![codecov](https://codecov.io/gh/uldyssian-sh/github-stats/branch/main/graph/badge.svg)](https://codecov.io/gh/uldyssian-sh/github-stats)

<div align="center">

```
┌─────────────────────────────────────────────────────────────┐
│                GitHub Statistics Dashboard                  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   GitHub    │────│ Data        │────│ Analytics   │     │
│  │    API      │    │ Collector   │    │  Engine     │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│         │                   │                   │          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ Repository  │    │ Contributor │    │ Dashboard   │     │
│  │  Metrics    │    │  Analytics  │    │  Reports    │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

</div>

## 🚀 Overview

Enterprise-grade GitHub repository analytics and statistics generator with automated CI/CD pipeline. Provides comprehensive insights into repository activity, contributor metrics, and project health indicators with enterprise security standards.

**Technology Stack:** Python 3.9+, GitHub GraphQL API v4, GitHub REST API v3, aiohttp, asyncio

## ✨ Key Features

- 📊 **Real-time Analytics** - Live GitHub repository statistics
- 🔄 **Automated Generation** - Daily automated stats updates via GitHub Actions
- 🛡️ **Enterprise Security** - Multi-layer security scanning and compliance
- 🎯 **Performance Optimized** - Async operations with rate limiting
- 📈 **Visual Reports** - SVG-based statistics visualization
- 🔍 **Code Quality** - Comprehensive quality metrics and analysis
- 🤖 **AI-Powered Workflows** - Intelligent automation and monitoring
- 🌐 **Free Tier Optimized** - Designed for GitHub Free tier limits

## 📊 Generated Statistics

### Overview Statistics
![GitHub Stats Overview](./generated/overview.svg)

### Language Distribution
![GitHub Languages](./generated/languages.svg)

## 🛠️ Prerequisites

- **Python**: 3.9 or higher
- **GitHub Token**: Personal Access Token with repo permissions
- **Git**: Command line tools
- **Internet**: Connection for GitHub API access

## 🚀 Quick Start

### Local Development

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

### GitHub Actions Integration

The repository automatically generates statistics daily via GitHub Actions. No manual intervention required.

## 📋 Available Metrics

### Repository Metrics
- ⭐ **Stargazers**: Total stars across all repositories
- 🍴 **Forks**: Total forks of user repositories
- 📝 **Contributions**: All-time contribution count
- 📊 **Repositories**: Number of repositories with contributions
- 📈 **Lines Changed**: Total lines added and deleted
- 👀 **Views**: Repository page views (last 14 days)

### Language Analysis
- 🔤 **Language Distribution**: Proportional usage by bytes
- 🎨 **Color Coding**: GitHub's official language colors
- 📊 **Percentage Breakdown**: Detailed language statistics
- 🔄 **Dynamic Updates**: Real-time language trend analysis

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|----------|
| `ACCESS_TOKEN` | GitHub Personal Access Token | ✅ | - |
| `GITHUB_ACTOR` | GitHub username | ✅ | - |
| `EXCLUDED` | Comma-separated list of repos to exclude | ❌ | `repo-private` |
| `EXCLUDED_LANGS` | Comma-separated list of languages to exclude | ❌ | `html,css` |
| `EXCLUDE_FORKED_REPOS` | Exclude forked repositories | ❌ | `true` |

### Advanced Configuration

```python
# Custom exclusions
EXCLUDED_REPOS = {'repo-private', 'test-repo'}
EXCLUDED_LANGS = {'html', 'css', 'dockerfile'}
EXCLUDE_FORKED_REPOS = True
```

## 🔒 Security & Compliance

### Security Features
- 🛡️ **Multi-layer Security Scanning**: CodeQL, Trivy, Bandit, Safety
- 🔍 **Secrets Detection**: TruffleHog integration
- 📋 **Dependency Review**: Automated vulnerability assessment
- 🔐 **Token Security**: Secure token management practices
- 📊 **SARIF Integration**: Security findings in GitHub Security tab

### Compliance Standards
- ✅ **GitHub Free Tier**: Optimized for free tier limits
- 🔒 **Data Privacy**: No sensitive data exposure
- 📝 **Audit Logging**: Comprehensive activity logging
- 🏢 **Enterprise Standards**: Professional DevOps practices

## 🤖 Automation & CI/CD

### Workflows
- **Enterprise CI/CD Pipeline**: Comprehensive testing and quality checks
- **Security Audit**: Weekly security scanning and vulnerability assessment
- **Stats Generator**: Daily automated statistics generation
- **Dependency Updates**: Automated dependency management via Dependabot

### Quality Gates
- Code formatting with Black
- Linting with Flake8 and Pylint
- Type checking with MyPy
- Security scanning with Bandit
- Test coverage reporting

## 📈 Performance & Optimization

- **Async Operations**: Non-blocking API calls with aiohttp
- **Rate Limiting**: Intelligent GitHub API rate limit handling
- **Caching**: Efficient data caching and retrieval
- **Error Handling**: Robust error recovery mechanisms
- **Resource Optimization**: Memory and CPU efficient processing

## 🔧 Development

### Code Quality Standards
```bash
# Format code
black .

# Lint code
flake8 .
pylint **/*.py

# Type checking
mypy .

# Security scan
bandit -r .

# Dependency check
safety check
```

### Testing
```bash
# Run tests with coverage
coverage run -m pytest -v
coverage report --show-missing
```

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Contributors
- **dependabot[bot]** - Automated dependency updates
- **actions-user** - GitHub Actions automation
- **uldyssian-sh LT** - Primary maintainer

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [GitHub Repository](https://github.com/uldyssian-sh/github-stats)
- [Issues](https://github.com/uldyssian-sh/github-stats/issues)
- [Pull Requests](https://github.com/uldyssian-sh/github-stats/pulls)
- [Actions](https://github.com/uldyssian-sh/github-stats/actions)
- [Security](https://github.com/uldyssian-sh/github-stats/security)

---

<div align="center">
  <strong>🚀 Powered by GitHub Actions | 🛡️ Enterprise Security | 🤖 AI-Driven Automation</strong>
</div>