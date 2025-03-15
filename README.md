# Scrapling Fetch MCP

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://img.shields.io/pypi/v/scrapling-fetch-mcp.svg)](https://pypi.org/project/scrapling-fetch-mcp/)

An MCP server that helps AI assistants access bot-protected websites, retrieving content in HTML or markdown format.

## Overview

This tool enables AI assistants to access content from websites that implement bot detection, bridging the gap between what you can see in your browser and what the AI can access.

> **Note**: This project was developed in collaboration with Claude Sonnet 3.7, using [LLM Context](https://github.com/cyberchitta/llm-context.py).

## Installation

1. Requirements:
   - Python 3.10+
   - [uv](https://github.com/astral-sh/uv) package manager

2. Install dependencies and the tool:
```bash
uv tool install scrapling
scrapling install
uv tool install scrapling-fetch-mcp
```

## Setup with Claude

Add this configuration to your Claude client's MCP server configuration:

```json
{
  "mcpServers": {
    "Cyber-Chitta": {
      "command": "uvx",
      "args": ["scrapling-fetch-mcp"]
    }
  }
}
```

## Example Usage

```
Human: Please fetch and summarize the documentation at https://example.com/docs

Claude: I'll help you with that. Let me fetch the documentation.

<mcp:function_calls>
<mcp:invoke name="scrapling-fetch">
<mcp:parameter name="url">https://example.com/docs</mcp:parameter>
<mcp:parameter name="mode">basic</mcp:parameter>
</mcp:invoke>
</mcp:function_calls>

Based on the documentation I retrieved, here's a summary...
```

## Functionality Options

- **Protection Levels**:
  - `basic`: Fast retrieval (1-2 seconds) but lower success with heavily protected sites
  - `stealth`: Balanced protection (3-8 seconds) that works with most sites
  - `max-stealth`: Maximum protection (10+ seconds) for heavily protected sites

- **Content Targeting**:
  - Retrieve entire pages or specific sections using regular expression search
  - Navigate large documents with pagination support

## Tips for Best Results

- Start with `basic` mode and only escalate to higher protection levels if needed
- For large documents, the AI can retrieve content in chunks
- Use the search functionality when looking for specific information on large pages
- The AI will automatically adjust its approach based on the site's protection level

## Limitations

- Not designed for high-volume scraping
- May not work with sites requiring authentication
- Performance varies by site complexity

## License

Apache 2
