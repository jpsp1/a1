from openai import OpenAI
from context import TWIN_SYSTEM_PROMPT
from tools import tools, handle_tool_calls
from styles import CSS, JS, EXAMPLES
from dotenv import load_dotenv
import gradio as gr
import os
import requests
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, trace, function_tool, SQLiteSession
import asyncio
import sys
from tools import notifier

load_dotenv(override=True)

MODEL_NAME = "gpt-5.4-mini"


# Make an agent with name, instructions, model

agent = Agent(name="Jokester", instructions="You are a joke teller", model=MODEL_NAME)


openai = OpenAI()

system = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}]


def chat(message, history):
    messages = system + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    while response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        tool_calls = message.tool_calls
        results = handle_tool_calls(tool_calls)
        messages.append(message)
        messages.extend(results)
        response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    return response.choices[0].message.content

async def main():
    with trace("Pizza has arrived"):
        result = await Runner.run(notifier, "Notify the user that the pizza is here")
        print(result.final_output)
    # Run the joke with Runner.run(agent, prompt)
    #result = await Runner.run(agent, "Tell a joke about Autonomous AI Agents")
    #print(result, flush=True)
    
if __name__ == "__main__":
    asyncio.run(main())
    sys.exit(0)
    gr.ChatInterface(
        chat,
        examples=EXAMPLES,
        title="Digital Twin",
        description="Talk to my AI twin about my career",
        chatbot=gr.Chatbot(show_label=False),
    ).launch(css=CSS, js=JS, share=True, 
    theme=gr.themes.Base())
