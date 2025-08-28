from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.tools.yfinance import YFinanceTools
import os

# Using GitHub Models - free models with just GitHub token!
agent = Agent(
    model=OpenAILike(
        id="gpt-4o-mini",
        api_key=os.getenv("GITHUB_TOKEN", "github_pat_your_token_here"),
        base_url="https://models.inference.ai.azure.com"
    ),
    tools=[YFinanceTools(stock_price=True)],
    instructions="Use tables to display data. Don't include any other text.",
    markdown=True,
)
agent.print_response("What is the stock price of Apple?", stream=True)
