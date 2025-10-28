# Plaid MCP Server

A Model Context Protocol (MCP) server that integrates Plaid's financial data API with Claude Desktop, enabling AI-powered financial insights and transaction analysis.

## Overview & Demo

This project bridges Claude Desktop and the Plaid API through an MCP server, allowing you to query financial data, analyze spending patterns, and retrieve transaction information directly through Claude's conversational interface.

https://github.com/user-attachments/assets/50d3435b-49d0-42e2-a3fc-2684ffc45944

## Technologies

- **Claude Desktop**: AI interface for interacting with financial data
- **Model Context Protocol (MCP)**: Standard protocol for connecting Claude with external tools
- **Express**: Node.js backend server handling API requests
- **Python**: MCP server implementation
- **Plaid API**: Financial data aggregation and account connectivity
- **Ngrok**: Secure tunneling to expose your local Express server to Claude Desktop

## Features

- Connect to multiple financial institutions via Plaid
- Retrieve account balances across all connected accounts
- Analyze spending by category and time period
- Search transactions by merchant or description
- Generate spending summaries with detailed breakdowns
- Seamless integration with Claude Desktop for natural language queries

## Prerequisites

Before getting started, ensure you have the following installed:

- Python 3.8 or higher
- Node.js and npm
- Plaid account with API credentials (get them at [plaid.com](https://plaid.com))
- Ngrok account for tunneling (sign up at [ngrok.com](https://ngrok.com))
- Claude Desktop installed on your system

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/plaid-mcp-server.git
cd plaid-mcp-server
```

### 2. Set Up the Express Backend

```bash
npm install
```

Create a `.env` file in the root directory with your Plaid credentials:

```
PLAID_CLIENT_ID=your_client_id
PLAID_SECRET=your_secret
PLAID_ENV=sandbox  # or 'development' / 'production'
```

### 3. Set Up the Python MCP Server

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### 1. Start the Express Server

```bash
uvicorn api.middleware:app --reload --port 8000
```

### 2. Start Ngrok Tunnel

In a new terminal:

```bash
ngrok http 8000
```

Ngrok will provide you with a public URL (e.g., `https://xxxx-xx-xxx-xxx-xx.ngrok.io`). Keep this running and note the URL.

### 4. Configure Claude Desktop

Add the MCP server to your Claude Desktop configuration. Update your `claude_desktop_config.json` (typically found in `~/.anthropic/` on macOS/Linux or `%APPDATA%\Anthropic\` on Windows):

```json
"mcpServers": {
    "Plaid Finance Inspector": {
      "id": "plaid-mcp",
      "name": "plaid-mcp-server",
      "command": "~/plaid-mcp-server/.venv/bin/python",
      "args": ["~/plaid-mcp-server/server.py"],
      "transport": "stdio"
    }
  }
```

### 5. Use with Claude Desktop

Open Claude Desktop and start asking about your finances:

- "What's my account balance?"
- "Show me my spending for the last month"
- "Search for all transactions at coffee shops"
- "What category did I spend the most on in the last three months?"

## Tools

- `get_hosted_link()` -  returns a secure Plaid link to authenticate bank account info and provide access to finanical data
- `get_spending_summary(time_range: str, category: str = None)` - aggregates transactions fetched from Plaid by category over a specified time range
- `get_account_balance()` - returns account balances accross all accounts stored in Plaid
- `search_transactions(search_term: str, limit: int = 10)` - returns all transactions under a specified category

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for bugs and feature requests.


## Support

For issues with Plaid integration, visit the [Plaid documentation](https://plaid.com/docs/). For MCP-related questions, check the [Model Context Protocol documentation](https://modelcontextprotocol.io/).
