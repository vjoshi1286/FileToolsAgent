import anthropic
from FileTools import execute_tool
from dotenv import load_dotenv
import json

#TODO externalize this json if possible
tools = [
    {
        "name": "list_files",
        "description": "List files in a directory, optionally filtered by a glob pattern.",
        "input_schema": {
            "type": "object",
            "properties": {
                "directory": {"type": "string", "description": "Directory path to list"},
                "pattern": {"type": "string", "description": "Glob pattern like '*.py'"}
            },
            "required": ["directory"]
        }
    },
    {
        "name": "read_file",
        "description": "Read the contents of a text file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path to read"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "search_in_files",
        "description": "Search for a text or pattern across files in a directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "directory": {"type": "string", "description": "Directory to search"},
                "pattern": {"type": "string", "description": "Text to search for"},
                "file_ext": {"type": "string", "description": "File extension filter, e.g., '.py'"}
            },
            "required": ["directory", "pattern"]
        }
    },
    {
        "name": "delete_file",
        "description": "Delete a given file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path to delete"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "append_to_file",
        "description": "Writes a given content to a file, optionally creates the file if not exists.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path to write to"},
                "content": {"type": "string", "description": "The content to be written"}
            },
            "required": ["path"]
        }
    }
]


def agent_loop(user_message):
    load_dotenv()
    client = anthropic.Anthropic()

    print(f"\nUser: {user_message}\n")
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  >> Tool Invocation : {block.name}({json.dumps(block.input)})")
                    result = execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:  # Terminate the agent loop
            for block in response.content:
                if hasattr(block, "text"):
                    print(f"Assistant: {block.text}")
            return
