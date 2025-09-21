"""Demonstrates tool-use: model calls browse web tool, then we judge the answer."""

from ai import complete_with_tools, openai
from browse_web import browse_web_tool_config

prompt = (
	"I want to buy a hoodie with a fur lined hood. It needs a full zipper. "
	"Near Times Square in NYC. Where can I buy one today at lunch time?"
)


def main():
	# Run with tool-choice enabled; tool calls are resolved automatically
	completion = complete_with_tools({
		"messages": [{"role": "developer", "content": prompt}],
		"model": "llama3.2:latest",
		"tool_choice": "auto",
		"tools": [browse_web_tool_config],
	})
	answer = completion.get("choices", [{}])[0].get("message", {}).get("content")
	print("\n\n" + "#" * 40)
	print(f"Answer: {answer}")

	# Judge completeness of the response
	check = openai.chat.completions.create({
		"model": "llama3.2:latest",
		"messages": [{
			"role": "developer",
			"content": (
				"You are a strict critic. Given the following question, determine if the answer a full answer to the question.\n\n"
				f"Question: {prompt}\n\nAnswer: {answer}"
			),
		}],
	})
	judge = check.get("choices", [{}])[0].get("message", {}).get("content", "").lower()
	is_done = "yes" in judge or "true" in judge or "complete" in judge
	print("\n\n" + "#" * 40)
	print(f"LLM as judge: {'👍' if is_done else '👎'}")


if __name__ == "__main__":
	main()
