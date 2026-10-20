# MCP (Model Context Protocol): A Primer

[中文](./MCP-Model-Context-Protocol.md) | English

- **Compiled**: 2026-10-20
- **Official resources**: [modelcontextprotocol.io](https://modelcontextprotocol.io/) · [Anthropic announcement (2024-11-25)](https://www.anthropic.com/news/model-context-protocol)
- **Test environment**: Python SDK `mcp` 2.3.0 and 1.30.0, Python 3.12, macOS

## 1. What is MCP

MCP (Model Context Protocol) is an open standard Anthropic introduced in November 2024 that lets AI models talk to external tools and data sources in one common "language". In December 2025, Anthropic donated MCP to the Agentic AI Foundation (AAIF, co-founded by Anthropic, Block and OpenAI) under the Linux Foundation, so the protocol is now vendor-neutral rather than owned by a single company.

Think of it as a **USB-C port**:

| | Without MCP | With MCP |
| --- | --- | --- |
| Integration | Custom integration code for every tool | The tool vendor builds one MCP server to the standard |
| Effort | 10 tools = 10 integrations | Build once, and every MCP-capable AI can use it |

## 2. The Roles

1. **Host**: the AI application itself, such as Claude Desktop, Claude Code and various AI coding tools.
2. **Client**: the host creates a separate client for **each** server, keeping a one-to-one connection. In everyday speech the host is often just called "the client", but in the official architecture the host is the application and the client is the connector inside it.
3. **Server**: a small program that "wraps" a tool or data source so AI can understand it, such as a GitHub server or a filesystem server.
4. **User**: decides which servers to connect and what the AI is allowed to do.

## 3. Three Kinds of Capabilities

| Type | What it is | Example |
| --- | --- | --- |
| Tools | Actions the AI can perform | Send an email, create a file |
| Resources | Data the AI can read | Documents, database records |
| Prompts | Ready-made common instructions | "Help me plan today's work" |

Each kind comes with matching discovery methods (`tools/list`, `resources/list`, `prompts/list`) and call methods: once connected to a server, the AI lists what is available, then calls what it needs.

## 4. Example Use Cases

- **Calendar + email**: "Find the day this week with the most meetings, and email that day's attendees a reminder to be on time." The AI reads the schedule through a calendar server → works out the busiest day → drafts and sends reminders through an email server.
- **Developers (GitHub)**: "See which issues in the repo are still open, and fix an easy one." The AI reads the issues, changes the code and opens a PR.
- **Data analysis (database)**: "Which product sold best last month?" The AI queries the database itself and answers, with no hand-written SQL.

## 5. Why It Matters

- **Less work**: a tool vendor builds once, and every AI can use it.
- **A shared ecosystem**: reuse MCP servers others have already written. Officially, the Python and TypeScript SDKs together see more than 97 million downloads a month.
- **Safe and controllable**: the user decides exactly what the AI can connect to and what it can do.

## 6. Hands-on: A To-do MCP Server (Python)

### 1. Install

```bash
pip install "mcp[cli]"   # requires Python 3.10+
```

### 2. Server code (todo_server.py)

```python
from mcp.server import MCPServer

mcp = MCPServer("todo")
todos = []

# Tools: actions the AI can perform
@mcp.tool()
def add_todo(task: str) -> str:
    """Add a to-do item"""
    todos.append({"task": task, "done": False})
    return f"Added: {task}"

@mcp.tool()
def complete_todo(index: int) -> str:
    """Mark to-do number `index` as done (counting from 1)"""
    if 1 <= index <= len(todos):
        todos[index - 1]["done"] = True
        return f"Done: {todos[index - 1]['task']}"
    return "No such item"

# Resources: data the AI can read
@mcp.resource("todo://list")
def get_todo_list() -> str:
    """All current to-do items"""
    if not todos:
        return "No to-dos yet"
    return "\n".join(
        f"{i}. [{'✓' if t['done'] else ' '}] {t['task']}"
        for i, t in enumerate(todos, 1)
    )

# Prompts: ready-made instructions
@mcp.prompt()
def daily_plan() -> str:
    return "Read my to-do list and help me order today's work by priority."

if __name__ == "__main__":
    mcp.run()  # talks to the AI app over stdio by default
```

### 3. Version pitfall: FastMCP has been renamed

Many tutorials online use `from mcp.server.fastmcp import FastMCP`. That is the SDK 1.x way; 2.x renamed `FastMCP` to `MCPServer`, and the old import fails with `ModuleNotFoundError`. Two options:

- Use the new version (recommended): `from mcp.server import MCPServer`; the decorators stay the same.
- Keep running old code: install `pip install "mcp[cli]<2"` to stay on 1.x.

### 4. Key Points

- `@mcp.tool()`: turns an ordinary function into a tool the AI can call.
- **The docstring matters**: the AI relies on it to understand what the tool does and when to use it; in testing, it is exactly the `description` field in the tool list.
- **Type hints become the parameter schema automatically**: `task: str` produces `{"task": {"type": "string"}}` and marks it as required. The SDK also validates arguments before the function runs, so a wrong type returns an error without ever entering the function body.
- **Never use `print()` in STDIO mode**: stdout is the protocol channel, and printing corrupts the JSON-RPC messages and breaks the server outright. For logs, use the standard `logging` module, which writes to stderr.

### 5. Local Debugging

```bash
mcp dev todo_server.py
```

This launches MCP Inspector, a web-based debugger where you can call tools by hand and inspect the results. Two prerequisites: Node.js must be installed (Inspector is fetched through npx, and the first download takes a dozen seconds or so), and on startup the terminal prints an address with an auth token, like `http://127.0.0.1:6274?MCP_INSPECTOR_API_TOKEN=...`; you have to open that full link to get in.

### 6. Connecting to Claude Desktop

Config file location:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "todo": {
      "command": "/your/path/.venv/bin/python",
      "args": ["/your/path/todo_server.py"]
    }
  }
}
```

Don't set `command` to a bare `python`. Claude Desktop doesn't launch the server inside your terminal's venv, and macOS's built-in `/usr/bin/python3` is still 3.9, which can't even install mcp (the SDK needs 3.10+), so the server silently fails to start. Two reliable options: give the absolute path to the venv's python, or use a command that brings its own environment, such as `uv run --with "mcp[cli]" python`.

If you'd rather not edit the JSON by hand, `mcp install todo_server.py` writes it into the config for you.

After a restart, use it in conversation:

```text
You: Add three to-dos for me: write the weekly report, book flights, reply to the client's email
Claude: (calls add_todo three times) Added them for you...
```

## 7. How It Works

```text
You speak → Claude decides it needs a tool → calls add_todo over MCP
          → the function runs and returns a result → Claude replies in natural language
```

The SDK handles all the tedious parts: protocol communication, argument validation, tool descriptions. When a connection is set up, the two sides also negotiate a protocol version (the handshake settled on `2025-11-25` in testing), which is how old and new clients coexist.

## 8. Where to Go Next

- Replace the in-memory list with SQLite or a real database so data isn't lost.
- Call external APIs from your tools (weather, translation, internal company systems).
- Switch to the HTTP transport and run it as a remote service.

## 9. Test Log

On 2026-10-20, under Python 3.12, I wrote a client that does the full stdio handshake the way a host does, and ran the server above through it:

- **New SDK (2.3.0) + `MCPServer`**: everything passed. The tool list, resource reads and prompt template all worked; after three `add_todo` calls, reading `todo://list` returned the list with `✓` check marks, and `daily_plan` returned the ready-made instruction with `role=user`.
- **Old SDK (1.30.0) + `FastMCP`**: also passed in full, with identical behavior.
- **New SDK + `FastMCP`**: fails on import. The SDK's error message is helpful: it points straight to the rename and to downgrading as the two ways out.
- **Argument validation**: `complete_todo(index="abc")` returns `isError: true` with a pydantic validation error, and the function never runs; an out-of-range call like `complete_todo(9)` is the function's own logic and returns "No such item" normally. The split between the two kinds of error is worth noting: the SDK catches types, but business rules are yours to write.

## In One Sentence

MCP is a "universal port" for AI: it lets AI use all kinds of tools and data safely and in a standard way, turning it from something that "only chats" into something that "actually gets work done".
