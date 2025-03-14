# Scrapling Fetch MCP Server

A simple Model Context Protocol (MCP) server implementation that integrates with [Scrapling](https://github.com/D4Vinci/Scrapling) for retrieving web content with advanced bot detection avoidance.

## Intended Use

This tool is optimized for low volume retrieval of documentation and reference materials from websites that implement bot detection. It has not been designed or tested for general-purpose site scraping or data harvesting.

## Features

* Retrieve content from websites that implement advanced bot protection
* Three protection levels (basic, stealth, max-stealth)
* Two output formats (HTML, markdown)

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
      "args": ["scrapling-fetch-mcp"]
    }
  }
}
```

## Available Tools

### fetch_url

Fetch a URL with configurable bot-detection avoidance levels.

```json
{
  "name": "fetch_url",
  "arguments": {
    "url": "https://example.com",
    "mode": "stealth",
    "format": "markdown"
  }
}
```

#### Parameters

- **url**: The URL to fetch
- **mode**: Protection level (options: `basic`, `stealth`, `max-stealth`)
  - `basic`: Fast retrieval with minimal protection
  - `stealth`: Balanced protection against bot detection
  - `max-stealth`: Maximum protection with all anti-detection features
- **format**: Output format (options: `html`, `markdown`)

## License

Apache 2
