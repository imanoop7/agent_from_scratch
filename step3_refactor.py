"""Refactored tool-run using shared registry and the tool loop."""

import index as tools
from ai import complete_with_tools, openai


goal = "I want to buy a hoodie with a fur lined hood. It needs a full zipper. Near Times Square in NYC. Where can I buy one today at lunch time?"

prompt = f"""
You are a helpful assistant working for a busy executive.
Your tone is friendly but direct, they prefer short clear and direct writing.
You try to accomplish the specific task you are given.
You can use any of the tools available to you.
Before you do any work you always make a plan using your Todo list.
You can mark todos off on your todo list after they are complete.

You summarize the actions you took by checking the done list then create a report.
You always ask your assistant to checkGoalDone. If they say you are done you send the report to the user.
If your assistant has feedback you add it to your todo list.

Today is PLACEHOLDER_DATE
"""


def main():
	# Use the shared tools registry; the loop resolves tool calls recursively
	completion = complete_with_tools({
		"messages": [
			{"role": "developer", "content": prompt},
			{"role": "user", "content": goal},
		],
		"model": "llama3.2:latest",
		"tool_choice": "auto",
		"tools": tools.configsArray,
	})
	answer = completion.get("choices", [{}])[0].get("message", {}).get("content")
	print("\n\n" + "#" * 40)
	print(f"Answer: {answer}")


if __name__ == "__main__":
	main()
