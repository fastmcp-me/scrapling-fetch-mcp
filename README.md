# Scrapling Fetch MCP Server

A simple Model Context Protocol (MCP) server implementation that integrates with [Scrapling](https://github.com/D4Vinci/Scrapling) for retrieving web content with advanced bot detection avoidance.

## Intended Use

This tool is optimized for low volume retrieval of documentation and reference materials (text/html only) from websites that implement bot detection. It has not been designed or tested for general-purpose site scraping or data harvesting.

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
uv tool install scrapling-fetch-mcp
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

### scrapling-fetch

Fetch a URL with configurable bot-detection avoidance levels.

```json
{
  "name": "scrapling-fetch",
  "arguments": {
    "url": "https://example.com",
    "mode": "stealth",
    "format": "markdown",
    "max_length": 5000,
    "start_index": 0
  }
}
```

#### Parameters

- **url** (required): The URL to fetch
- **mode** (optional, default: "basic"): Protection level
  - `basic`: Fast retrieval with minimal protection
  - `stealth`: Balanced protection against bot detection
  - `max-stealth`: Maximum protection with all anti-detection features
- **format** (optional, default: "markdown"): Output format (options: `html`, `markdown`)
- **max_length** (optional, default: 5000): Maximum number of characters to return
- **start_index** (optional, default: 0): Character index to start from in the response (useful for paginated content)

## License

Apache 2
