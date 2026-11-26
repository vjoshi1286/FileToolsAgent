import json
from pathlib import Path
from typing import Any

def get_tools() -> list[dict[str, Any]]:
    tools_path = Path(__file__).parent / "tools.json"
    with open(tools_path, "r", encoding="utf-8") as file:
        return json.load(file)
