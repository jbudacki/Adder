def execute_model_action(model_output: dict) -> dict:
    tool_name = model_output["tool"]
    arguments = model_output["arguments"]
    return {"tool": tool_name, "arguments": arguments, "status": "simulated"}

