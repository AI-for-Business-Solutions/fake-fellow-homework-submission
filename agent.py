import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from tools import TOOLS, TOOL_FUNCTIONS

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com"
)

def call_llm(messages):
    response = client.chat.completions.create(
        model="deepseek-v4-flash", messages=messages, tools=TOOLS
    )
    return response.choices[0].message

def run_tool(name, args_json):
    print("Calling tool:", name)
    args = json.loads(args_json)
    return TOOL_FUNCTIONS[name](**args)

def agent_loop(messages):
    for _ in range(5):
        message = call_llm(messages)
        messages.append(message.model_dump())

        if not message.tool_calls:
            return message.content

        for tool_call in message.tool_calls:
            result = run_tool(tool_call.function.name, tool_call.function.arguments)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result),
            })

def main():
    messages = [
        {"role": "system", "content": "You are an HR support agent. Answer questions about employees and PTO using the tools."}
    ]
    print("HR Support Agent (type exit to quit)\n")

    while True:
        user_input = input("User> ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye.")
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        answer = agent_loop(messages)
        print("Agent>", answer, "\n")

if __name__ == "__main__":
    main()
