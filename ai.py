"""Lightweight Ollama client shim and tool-call loop.

Targets Ollama's OpenAI-compatible `/v1/chat/completions` endpoint and provides
`complete_with_tools`, which repeatedly handles function/tool calls until the
model returns a final assistant message.
"""

import os
import json
import requests
from typing import Any, Dict, List

# Local tools registry imported lazily to avoid circular imports

def _get_base_url() -> str:
	"""Return base URL for the Ollama OpenAI-compatible API.

	Falls back to the default local service if no environment variable is set.
	"""
	return os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")


def _post_chat_completions(payload: Dict[str, Any]) -> Dict[str, Any]:
	"""POST the chat completion request to Ollama and return parsed JSON.

	Includes a fallback: if the server returns HTTP 400 and the payload contains
	tools/tool_choice, retry once without tool-related fields (some models or
	servers may not accept tool schema).
	"""
	url = f"{_get_base_url()}/chat/completions"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {os.getenv('OLLAMA_API_KEY', 'ollama')}"
	}
	resp = requests.post(url, headers=headers, json=payload, timeout=300)
	if resp.status_code == 400 and ("tools" in payload or "tool_choice" in payload):
		# Retry without tools
		fallback = {k: v for k, v in payload.items() if k not in ("tools", "tool_choice")}
		resp = requests.post(url, headers=headers, json=fallback, timeout=300)
	resp.raise_for_status()
	return resp.json()


class OllamaClient:
	"""Minimal interface to resemble `openai.chat.completions.create` usage."""

	def __init__(self):
		pass

	class chat:
		class completions:
			@staticmethod
			def create(args: Dict[str, Any]) -> Dict[str, Any]:
				"""Forward request to Ollama's chat completions endpoint."""
				return _post_chat_completions(args)


openai = OllamaClient()


def complete_with_tools(args: Dict[str, Any]) -> Dict[str, Any]:
	"""Run a chat completion and automatically fulfill any tool calls.

	- Sends `args` as-is to the model (expects OpenAI-style schema).
	- If the model returns tool/function calls, looks them up in
	  `index.functions`, executes them, and appends the results
	  as `role="tool"` messages.
	- Repeats until the model returns a normal assistant message without tools.
	"""
	# Log truncated last message for visibility
	try:
		last_msg = args["messages"][len(args["messages"]) - 1]
		print(f"Calling llm with: {json.dumps(last_msg)[:500]}")
	except Exception:
		pass

	completion = openai.chat.completions.create(args)

	choice0 = completion.get("choices", [{}])[0]
	message = choice0.get("message", {})
	tool_calls = message.get("tool_calls")

	if tool_calls:
		# Lazy import tool registry from project root
		from index import functions as tool_functions

		# Persist the model's function-call message for traceability
		args["messages"].append(message)

		for tool_call in tool_calls:
			fn_name = tool_call.get("function", {}).get("name")
			fn_args_raw = tool_call.get("function", {}).get("arguments", "{}")
			try:
				fn_args = json.loads(fn_args_raw)
			except Exception:
				fn_args = {}

			print("\n\n" + "#" * 40)
			print(f"tool_calling: {fn_name}({json.dumps(fn_args)})")
			result = tool_functions[fn_name](fn_args)

			# Attach the tool result so the model can continue reasoning
			args["messages"].append({
				"role": "tool",
				"tool_call_id": tool_call.get("id", ""),
				"content": result,
			})

		# Continue until there are no further tool calls
		return complete_with_tools(args)

	print("\n\n" + "#" * 40)
	content = message.get("content", "")
	print(content[:500])
	return completion
