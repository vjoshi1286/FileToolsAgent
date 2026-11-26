import anthropic
from dotenv import load_dotenv
import os
import json

from toolreader import get_tools
from filetools import execute_tool

#TODO refactor this code

def agent_loop(user_message):
    
    load_dotenv()
    
    client = anthropic.Anthropic()

    print(f"\nUser: {user_message}\n")
    messages = [{"role": "user", "content": user_message}]
    
    tools = get_tools()
    # print(tools)

    llm = os.getenv("LLM")
    max_tokens = int(os.getenv("MAX_TOKENS",4096))

    system_prompt =""" Give PRECISE answers, max 2 lines
        describe multiple files in <file_name>:<description> format description should be in max 2 lines
        Append the markers like TODO/FIXME store the content as <line_nuber> : <stripped_text_after_marker>
        Search directories only 1 level, DO NOT search sub-directories 
        While appending a string content which is json, ALWAYS extract the content part
    """

    while True:
        response = client.messages.create(
            model      = llm,
            max_tokens = max_tokens,
            tools      = tools,
            system     = system_prompt,
            messages   = messages 
            #Context keeps on increasing here
        )

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  >> Tool Call : {block.name}({json.dumps(block.input)})")
                    result = execute_tool(block.name, block.input)
                    
                   # print(f"Tool result : {result}")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            # The whole of the conversation is given to the LLM
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        
        else:  # Terminate the agent loop
            for block in response.content:
                if hasattr(block, "text"):
                  return block.text    
            return "Empty"
