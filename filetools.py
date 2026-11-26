import glob
import json
import os

#TODO cleanup and refactor the file

# LLM just returns us the tool_call intent, how to execute it, is upto us

def execute_tool(name, args):
    tools_dir = {
        "list_files": lambda d: list_files(d["directory"], d.get("pattern")),
        "read_file": lambda d: read_file(d["path"]),
        "search_in_files": lambda d: search_in_files(d["directory"], d["pattern"], d.get("file_ext")),
        "delete_file": lambda d: delete_file(d["path"]),
        "append_to_file": lambda d: append_to_file(d["path"],d["content"]),
        "extract_content": lambda d: extract_content(d["message"])
    }

    return tools_dir.get(name, lambda d: json.dumps({"error": "Unidentified tool"}))(args)

def extract_content(message):
    data = json.loads(message)
    content = data.get("content")
    return content

def list_files(directory, pattern=None):
    try:
        if pattern:
            files = glob.glob(os.path.join(directory, "**", pattern), recursive=True)
        else:
            files = os.listdir(directory)
        return json.dumps({"files": sorted(files), "count": len(files)})
    except Exception as e:
        return json.dumps({"error": str(e)})

def append_to_file(path, content):
   try: 
     with open("example.txt", "a") as file:
       file.write(content)
     return json.dumps({"path", path})
   except Exception as e:
     return json.dumps({"error": str(e)})

def read_file(path):
    try:
        with open(path, "r") as f:
            content = f.read()
        return json.dumps({"path": path, "content": content[:10000], "lines": content.count("\n") + 1})
    except Exception as e:
        return json.dumps({"error": str(e)})


def search_in_files(directory, pattern, file_ext=None):
    results = []
    for root, dirs, files in os.walk(directory):
        for fname in files:
            if file_ext and not fname.endswith(file_ext):
                continue
            filepath = os.path.join(root, fname)
            try:
                with open(filepath, "r") as f:
                    for i, line in enumerate(f, 1):
                        if pattern.lower() in line.lower():
                            results.append({"file": filepath, "line": i, "text": line.strip()})
            except (UnicodeDecodeError, PermissionError):
                continue
    return json.dumps({"matches": results[:50], "total": len(results)})


def delete_file(path):
    try:
        os.remove(path)
        return json.dumps({"path" : path})
    except Exception as e:
        return json.dumps({"error": str(e)})



