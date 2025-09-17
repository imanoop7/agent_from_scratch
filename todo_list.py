"""In-memory todo list tools.

These functions are intentionally stateful within process memory to make it
trivial for an LLM agent to plan, act, and track progress in a single run.
"""

import json
from typing import List, Dict, Any

_todos: List[str] = []
_done: List[str] = []


def add_todos(params: Dict[str, Any]) -> str:
	"""Append new todos and print the current list for visibility."""
	new_todos = params.get("newTodos", [])
	_todos.extend(new_todos)
	delim = "\n  - "
	print(f"Todo list:{delim}{delim.join(_todos)}")
	return f"Added {len(new_todos)} to todo list. Now have {_todos.__len__()} todos."


add_todos_tool_config = {
	"type": "function",
	"function": {
		"name": "addTodos",
		"description": "Add an array of todos to my todo list.",
		"parameters": {
			"type": "object",
			"properties": {
				"newTodos": {
					"type": "array",
					"items": {"type": "string"},
					"description": "The array of new todos to add to my todo list."
				}
			},
			"required": ["newTodos"],
		}
	}
}


def mark_todo_done(params: Dict[str, Any]) -> str:
	"""Mark a todo as done; keep a separate done list for summarization."""
	todo = params.get("todo")
	global _todos
	if todo in _todos:
		_todos = [t for t in _todos if t != todo]
		_done.append(todo)
		return f"Marked the following todo as done:\n  {todo}"
	else:
		return f"Todo list doesn't include todo:\n  {todo}"


mark_todo_done_tool_config = {
	"type": "function",
	"function": {
		"name": "markTodoDone",
		"description": "Mark an individual item on my todo list as done.",
		"parameters": {
			"type": "object",
			"properties": {
				"todo": {
					"type": "string",
					"description": "The array of new todos to add to my todo list."
				}
			},
			"required": ["todo"],
		}
	}
}


def check_todos(_: Dict[str, Any]) -> str:
	"""Return todos as JSON, or a user-friendly empty message."""
	return "The todo list is empty." if len(_todos) == 0 else json.dumps(_todos)


check_todos_tool_config = {
	"type": "function",
	"function": {
		"name": "checkTodos",
		"description": "Read everything on the todo list.",
		"parameters": {
			"type": "object",
			"properties": {},
			"additionalProperties": False,
		}
	}
}
