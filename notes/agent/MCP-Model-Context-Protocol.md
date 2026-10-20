# MCP (Model Context Protocol) 入门整理

- **整理日期**: 2026-10-20
- **官方资料**: [modelcontextprotocol.io](https://modelcontextprotocol.io/) · [Anthropic 发布公告 (2024-11-25)](https://www.anthropic.com/news/model-context-protocol)
- **实测环境**: Python SDK `mcp` 2.3.0 与 1.30.0，Python 3.12，macOS

## 一、MCP 是什么

MCP（模型上下文协议）是 Anthropic 2024 年 11 月推出的开放标准，让 AI 模型和外部工具、数据源用同一种「语言」沟通。2025 年 12 月，Anthropic 把 MCP 捐给了 Linux Foundation 下的 Agentic AI Foundation（AAIF，由 Anthropic、Block、OpenAI 共同发起），协议从此中立化，不再属于单一厂商。

类比 **USB-C 接口**：

| | 没有 MCP | 有了 MCP |
| --- | --- | --- |
| 对接方式 | 每个工具单独开发一套对接代码 | 工具方按标准做一个 MCP 服务器 |
| 工作量 | 对接 10 个工具 = 写 10 套 | 一次开发，所有支持 MCP 的 AI 都能用 |

## 二、三个角色

1. **宿主（Host）**：AI 应用本身，如 Claude Desktop、Claude Code、各类 AI 编程工具。
2. **客户端（Client）**：宿主为**每一个**服务器单独创建一个客户端，一对一维持连接。日常口语里常把宿主直接叫「客户端」，但按官方架构，宿主是应用，客户端是应用内的连接器。
3. **服务器（Server）**：把某个工具或数据「包装」成 AI 能理解的小程序，如 GitHub 服务器、文件系统服务器。
4. **用户**：决定连接哪些服务器、授权 AI 能做什么。

## 三、MCP 提供的三类能力

| 类型 | 说明 | 示例 |
| --- | --- | --- |
| 工具（Tools） | AI 可以执行的操作 | 发邮件、创建文件 |
| 资源（Resources） | AI 可以读取的数据 | 文档、数据库记录 |
| 提示模板（Prompts） | 预设好的常用指令 | 「帮我安排今天的工作」 |

三类能力都有配套的发现方法（`tools/list`、`resources/list`、`prompts/list`）和调用方法，AI 连上服务器后先列清单，再按需调用。

## 四、使用场景举例

- **日历 + 邮件**：「看看这周哪天会最多，给那天的参会人发邮件提醒准时。」 AI 通过日历服务器读日程 → 分析出最忙的一天 → 通过邮件服务器起草并发送提醒。
- **程序员（GitHub）**：「看看仓库里有哪些未解决的 issue，挑个简单的修一下。」 AI 读 issue、改代码、提交 PR。
- **数据分析（数据库）**：「上个月哪个产品卖得最好？」 AI 自己查数据库并给出答案，无需手写 SQL。

## 五、为什么重要

- **省事**：工具方做一次，所有 AI 通用。
- **生态共享**：可复用他人写好的 MCP 服务器。官方公布 Python 与 TypeScript SDK 月下载量合计超过 9700 万次。
- **安全可控**：用户明确决定 AI 能连什么、做什么。

## 六、开发示例：待办事项 MCP 服务器（Python）

### 1. 安装

```bash
pip install "mcp[cli]"   # 需要 Python 3.10 以上
```

### 2. 服务器代码（todo_server.py）

```python
from mcp.server import MCPServer

mcp = MCPServer("todo")
todos = []

# 工具：AI 可执行的操作
@mcp.tool()
def add_todo(task: str) -> str:
    """添加一条待办事项"""
    todos.append({"task": task, "done": False})
    return f"已添加：{task}"

@mcp.tool()
def complete_todo(index: int) -> str:
    """把第 index 条待办标记为完成（从 1 开始数）"""
    if 1 <= index <= len(todos):
        todos[index - 1]["done"] = True
        return f"已完成：{todos[index - 1]['task']}"
    return "编号不存在"

# 资源：AI 可读取的数据
@mcp.resource("todo://list")
def get_todo_list() -> str:
    """当前所有待办事项"""
    if not todos:
        return "暂无待办"
    return "\n".join(
        f"{i}. [{'✓' if t['done'] else ' '}] {t['task']}"
        for i, t in enumerate(todos, 1)
    )

# 提示模板：预设指令
@mcp.prompt()
def daily_plan() -> str:
    return "请读取我的待办清单，帮我按优先级安排今天的工作顺序。"

if __name__ == "__main__":
    mcp.run()  # 默认通过 stdio 与 AI 应用通信
```

### 3. 版本坑：FastMCP 已改名

网上大量教程写的是 `from mcp.server.fastmcp import FastMCP`。那是 SDK 1.x 的写法，2.x 把 `FastMCP` 改名成了 `MCPServer`，旧写法会直接报 `ModuleNotFoundError`。两种选择：

- 用新版（推荐）：`from mcp.server import MCPServer`，其余装饰器写法不变。
- 继续跑旧代码：装 `pip install "mcp[cli]<2"` 锁在 1.x。

### 4. 关键点

- `@mcp.tool()`：把普通函数变成 AI 可调用的工具。
- **docstring 很重要**：AI 靠它理解工具用途和使用时机，实测它就是工具清单里的 `description` 字段。
- **类型标注会自动转成参数说明**：`task: str` 生成 `{"task": {"type": "string"}}` 并标记为必填。SDK 还会在函数执行前校验参数，传错类型直接返回错误，不会进到函数体。
- **STDIO 模式下绝对不能用 `print()`**：stdout 是协议通道，打印会污染 JSON-RPC 消息、直接搞坏服务器。要输出日志就用标准库 `logging`，它走 stderr。

### 5. 本地调试

```bash
mcp dev todo_server.py
```

会启动网页版调试器 MCP Inspector，可手动调用工具、查看返回结果。两个前提：机器上要有 Node.js（Inspector 靠 npx 拉取，首次下载约十几秒），启动后终端会打印带 auth token 的地址，形如 `http://127.0.0.1:6274?MCP_INSPECTOR_API_TOKEN=...`，要用这个完整链接才能访问。

### 6. 接入 Claude Desktop

配置文件位置：

- macOS：`~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows：`%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "todo": {
      "command": "/你的路径/.venv/bin/python",
      "args": ["/你的路径/todo_server.py"]
    }
  }
}
```

`command` 这里别写成光秃秃的 `python`。Claude Desktop 启动服务器时不走你终端里的 venv，macOS 自带的 `/usr/bin/python3` 还是 3.9，连 mcp 都装不上（SDK 要求 3.10+），服务器会静默起不来。两个稳妥写法：填 venv 里 python 的绝对路径，或者用 `uv run --with "mcp[cli]" python` 这类自带环境的命令。

懒得手改 JSON 的话，`mcp install todo_server.py` 会自动写进配置。

重启后即可对话使用：

```text
你：帮我加三条待办：写周报、订机票、回复客户邮件
Claude：（调用 add_todo 三次）已为你添加……
```

## 七、运行原理

```text
你说话 → Claude 判断需要用工具 → 通过 MCP 协议调用 add_todo
      → 函数执行并返回结果 → Claude 用自然语言回复你
```

协议通信、参数校验、工具描述等繁琐工作，全部由 SDK 处理。连接建立时双方还会协商协议版本（实测握手结果是 `2025-11-25`），所以新旧客户端能共存。

## 八、进阶方向

- 将内存列表换成 SQLite 或真实数据库，数据不丢失。
- 在工具里调用外部 API（天气、翻译、公司内部系统）。
- 改用 HTTP 传输方式，做成远程服务。

## 九、实测记录

2026-10-20 在 Python 3.12 下写了个客户端，按宿主的方式走完整 stdio 握手，把上面的服务器跑了一遍：

- **新版 SDK（2.3.0）+ `MCPServer` 写法**：全部通过。工具清单、资源读取、提示模板都正常，`add_todo` 三次后读 `todo://list` 返回带 `✓` 勾选状态的列表，`daily_plan` 返回 `role=user` 的预设指令。
- **旧版 SDK（1.30.0）+ `FastMCP` 写法**：同样全部通过，行为一致。
- **新版 SDK + `FastMCP` 写法**：导入即失败。SDK 给的报错信息很友好，直接提示改名和降级两条路。
- **参数校验**：`complete_todo(index="abc")` 返回 `isError: true` 和 pydantic 校验错误，函数没被执行；而 `complete_todo(9)` 这种越界是函数自己的逻辑，正常返回「编号不存在」。两类错误的分工值得注意——类型由 SDK 挡，业务规则得自己写。

## 一句话总结

MCP 就是给 AI 装的「万能接口」，让它能安全、标准化地使用各种工具和数据，从「只会聊天」变成「能真正帮你干活」。
