# Scrapling MCP Server

A Model Context Protocol (MCP) server implementation that integrates with [Scrapling](https://github.com/D4Vinci/Scrapling) for retrieving web content with advanced bot detection avoidance.

## Intended Use

This tool is optimized for retrieving documentation and reference materials from websites. It has not been designed or tested for general-purpose site scraping or data harvesting.

## Features

* Retrieve content from websites that implement advanced bot protection
* Multiple browser options (basic, stealth)
* Multiple output formats (text, HTML)

## Installation

### Install scrapling

```bash
uv tool install scrapling
scrapling install
```

```bash
uv tool install scrapling-mcp
```

## Usage with Claude

Add this configuration to your Claude client's MCP server configuration:

```json
{
  "mcpServers": {
    "Cyber-Chitta": {
      "command": "uvx",
      "args": ["scrapling-mcp"]
    }
  }
}
```

## Available Tools

### scrapling_browse_quick

Scrape a webpage with configurable bot-detection avoidance.

```json
{
  "name": "scrapling_browse_quick",
  "arguments": {
    "url": "https://example.com",
    "browser_type": "stealth",
    "selector": ".content",
    "format": "text"
  }
}
```

### scrapling_browse_stealth

Scrape a webpage with adaptive element selection that can survive website structure changes.

```json
{
  "name": "scrapling_browse_stealth",
  "arguments": {
    "url": "https://example.com",
    "selector": ".product-list",
    "auto_save": true,
    "auto_match": true,
    "format": "text"
  }
}
```

## Development

Clone the repository:

```bash
git clone https://github.com/cyberchitta/scrapling-mcp.git
cd scrapling-mcp
```

Set up the development environment:

```bash
pip install -e ".[dev]"
```

Run the tests:

```bash
pytest
```

## License

Apache 2
