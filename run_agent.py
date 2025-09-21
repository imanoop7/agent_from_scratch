"""Run a single agent with planning and tools.

This script provides a simple CLI wrapper around the tool loop. It uses the
shared tool registry (index.py) and the Ollama OpenAI-compatible API via
ai.complete_with_tools.

Example:
  python run_agent.py --goal "Find a coffee shop near Times Square open now"

Environment:
  OLLAMA_BASE_URL (optional) - defaults to http://localhost:11434/v1
  OLLAMA_API_KEY  (optional) - defaults to "ollama" (not validated by Ollama)
"""

from __future__ import annotations

import argparse
from datetime import datetime

import index as tools
from ai import complete_with_tools


def build_prompt(now: datetime) -> str:
    return f"""
You are a helpful assistant working for a busy executive.
Your tone is friendly but direct, they prefer short, clear, and direct writing.
You try to accomplish the specific task you are given.
You can use any of the tools available to you.
Before you do any work you always make a plan using your Todo list.
You can mark todos off on your todo list after they are complete.

You summarize the actions you took by checking the done list then create a report.
You always ask your assistant to checkGoalDone. If they say you are done you send the report to the user.
If your assistant has feedback you add it to your todo list.

Today is {now}
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a single planning agent using local tools.")
    parser.add_argument("--goal", required=True, help="User goal or request to complete.")
    parser.add_argument(
        "--model",
        default="llama3.2:latest",
        help="Model name as known by your Ollama server (default: %(default)s)",
    )
    args = parser.parse_args()

    prompt = build_prompt(datetime.now())

    completion = complete_with_tools({
        "messages": [
            {"role": "developer", "content": prompt},
            {"role": "user", "content": args.goal},
        ],
        "model": args.model,
        "tool_choice": "auto",
        "tools": tools.configsArray,
    })

    answer = completion.get("choices", [{}])[0].get("message", {}).get("content", "")
    print("\n\n" + "#" * 40)
    print(f"Answer: {answer}")


if __name__ == "__main__":
    main()
