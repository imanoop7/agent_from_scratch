"""LLM-based goal checker using the same tool loop.

Asks the model to evaluate whether an answer satisfies a goal and to provide
actionable feedback if not complete. Returns a JSON string for easy consumption.
"""

import json
from typing import Dict, Any
from ai import complete_with_tools

_prompt = (
	"\nYou are research assistant who reads requests and answers.\n"
	"You determine if the answer satisfies the request.\n"
	"If it does you respond that the request is done.\n"
	"If not you give specific feedback on what is missing in the form of actionable individual todos.\n"
)


def check_goal_done(params: Dict[str, Any]) -> str:
	"""Return a JSON string with fields: { done: bool, feedback: string[] }."""
	goal = params.get("goal", "")
	answer = params.get("answer", "")
	resp = complete_with_tools({
		"model": "llama3.2:latest",
		"messages": [
			{"role": "developer", "content": _prompt},
			{"role": "user", "content": f"## Request: {goal}\n\n## Answer: {answer}"},
		],
	})
	msg = resp.get("choices", [{}])[0].get("message", {})
	content = (msg.get("content") or "").strip()
	# Attempt to parse the model output; fall back to a safe default.
	try:
		parsed = json.loads(content)
	except Exception:
		parsed = {"done": False, "feedback": ["Could not parse judge response."]}
	print("\n\n" + "#" * 40)
	print(f"LLM as judge: {'👍' if parsed.get('done') else '👎'}")
	return json.dumps(parsed)


check_goal_done_tool_config = {
	"type": "function",
	"function": {
		"name": "checkGoalDone",
		"description": "Check if the answer successfully meets the requested goal.",
		"parameters": {
			"type": "object",
			"properties": {
				"goal": {"type": "string", "description": "The requested goal to be completed."},
				"answer": {"type": "string", "description": "The answer that will be provided to the requesting party to complete that goal."}
			},
			"required": ["goal", "answer"],
		}
	}
}
