ALLOWED_TOOLS = {"search"}


def execute_tool(tool_name: str, arguments: dict, approved: bool) -> dict:
    if tool_name not in ALLOWED_TOOLS:
        raise PermissionError("tool is outside the agent capability set")
    if not approved:
        raise PermissionError("human confirmation is required")
    return {"tool": tool_name, "arguments": arguments, "status": "simulated"}

