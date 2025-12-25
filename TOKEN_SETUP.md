# GitHub Token Setup Guide

## Problem
The GitHub stats generator needs proper API access to collect accurate statistics. The default `GITHUB_TOKEN` has limited permissions and rate limits.

## Solution: Personal Access Token

### 1. Create Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Set expiration to "No expiration" or 1 year
4. Select these scopes:
   - ✅ `public_repo` - Access public repositories
   - ✅ `read:user` - Read user profile data
   - ✅ `user:email` - Access user email addresses
   - ✅ `read:org` - Read organization membership

### 2. Add Token to Repository Secrets

1. Go to your repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `PERSONAL_ACCESS_TOKEN`
4. Value: Your generated token
5. Click "Add secret"

### 3. Verify Setup

Run the workflow manually or wait for the next scheduled run. Check the logs for:
- ✅ "Access token found - using authenticated API requests"
- ✅ "GraphQL API: 200"
- ✅ Higher rate limits (5000/hour instead of 60/hour)

## Alternative: Use GITHUB_TOKEN (Limited)

If you prefer not to use a personal access token, the workflow will fall back to the default `GITHUB_TOKEN` with these limitations:
- Lower rate limits (1000 requests/hour)
- No access to private repository data
- Some statistics may be estimated instead of exact

## Testing Token Locally

```bash
export GITHUB_ACTOR=uldyssian-sh
export ACCESS_TOKEN=your_token_here
python test_token.py
```

## Troubleshooting

### Rate Limit Exceeded
- Wait for rate limit reset (shown in error message)
- Use personal access token for higher limits
- Reduce frequency of workflow runs

### Authentication Failed
- Check token is valid and not expired
- Verify token has correct permissions
- Ensure token is properly set in repository secrets

### GraphQL Errors
- Personal access token required for GraphQL API
- Check token permissions include user data access