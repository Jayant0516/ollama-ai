import asyncio
import ollama
import json
from mcp.client.stdio import stdio_client
from mcp import ClientSession

SYSTEM_PROMPT = """
You are a planning agent.

Respond ONLY in this format:

THOUGHT: reasoning
ACTION: tool_name OR FINAL
INPUT: JSON or null

Use previous observations if needed.
"""

def parse(text):
    lines = text.splitlines()
    thought = lines[0][8:].strip()
    action = lines[1][7:].strip()
    raw_input = lines[2][6:].strip()

    args = None
    if raw_input.lower() != "null":
        args = json.loads(raw_input)
    return thought, action, args

async def run_agent(question):
    async with stdio_client(["python", "mcp_server.py"]) as (r, w):
        async with ClientSession(r, w) as session:

            tools = await session.list_tools()
            tool_desc = "\n".join(
                f"{t.name}: {t.description}" for t in tools.tools
            )

            messages = [{
                "role": "system",
                "content": SYSTEM_PROMPT + "\n\nTools:\n" + tool_desc
            }, {
                "role": "user",
                "content": question
            }]

            step = 0
            while True:
                step += 1
                print(f"\n--- Step {step} ---")

                reply = ollama.chat(
                    model="llama3",
                    messages=messages
                )["message"]["content"]

                print(reply)
                messages.append({"role": "assistant", "content": reply})

                thought, action, args = parse(reply)

                if action == "FINAL":
                    print("\n Done")
                    break

                # Sequential tool call
                result = await session.call_tool(action, args)

                observation = f"OBSERVATION: {result.content}"
                print(observation)

                messages.append({
                    "role": "user",
                    "content": observation
                })

if __name__ == "__main__":
    asyncio.run(run_agent(
        "Add 10 and 20, multiply the result by 3, then tell me the time"
    ))
