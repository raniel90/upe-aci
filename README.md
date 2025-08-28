# ACI - AI Agent Project

A Python project using the Agno framework to create AI agents with financial data capabilities.

## Features

- AI agent powered by GitHub Models (GPT-4o Mini)
- Free access to models using only GitHub Personal Access Token
- No paid API keys required!
- Stock price retrieval using YFinance
- Simple setup and deployment
- Poetry for dependency management

## Setup

1. Install dependencies:
   ```bash
   poetry install
   ```

2. Create a `.env` file with your GitHub token (optional):
   ```
   GITHUB_TOKEN=your_github_personal_access_token
   ```
   
   To get your GitHub Personal Access Token:
   - Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
   - Generate a new token (classic)
   - Select scopes: `public_repo` (minimum required)
   - Copy the token
   
   **Note**: If you don't set the token, the code includes a fallback, but it's recommended to use your own token for better rate limits.

3. Run the agent:
   ```bash
   poetry run python level_1_agent.py
   ```

## Dependencies

- `agno`: AI agent framework
- `python-dotenv`: Environment variable management (optional)
- `yfinance`: Financial data retrieval

## Why GitHub Models?

- ✅ **Free**: No paid API keys required
- ✅ **High Quality**: Access to GPT-4o Mini and other powerful models
- ✅ **Simple Setup**: Just need a GitHub account
- ✅ **No Local Installation**: Runs on Microsoft's infrastructure
- ✅ **Good Rate Limits**: Generous free tier for experimentation

## Development

- `pytest`: Testing framework
- `black`: Code formatting
- `flake8`: Code linting
