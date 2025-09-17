"""Tool registry and tool configs exposed for the LLM tool-use API."""

from todo_list import (
	add_todos, add_todos_tool_config,
	mark_todo_done, mark_todo_done_tool_config,
	check_todos, check_todos_tool_config,
)
from llm_judge import check_goal_done, check_goal_done_tool_config
from browse_web import browse_web, browse_web_tool_config

functions = {
	"addTodos": add_todos,
	"markTodoDone": mark_todo_done,
	"checkTodos": check_todos,
	"checkGoalDone": check_goal_done,
	"browseWeb": browse_web,
}

configsArray = [
	add_todos_tool_config,
	mark_todo_done_tool_config,
	check_todos_tool_config,
	check_goal_done_tool_config,
	browse_web_tool_config,
]
