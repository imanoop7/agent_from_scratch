"""Two-call pattern: generate answer, then judge completeness."""

from ai import openai

prompt = "What is the average wing speed of a swallow?"


def main():
	print("\n\n" + "#" * 40)
	print(f"Question: {prompt}")

	# First: get an answer
	completion = openai.chat.completions.create({
		"messages": [{"role": "developer", "content": prompt}],
		"model": "llama3.2:latest",
	})
	answer = completion.get("choices", [{}])[0].get("message", {}).get("content")
	print("\n\n" + "#" * 40)
	print(f"Answer: {answer}")

	# Second: ask a judge prompt to assess completeness
	check = openai.chat.completions.create({
		"model": "llama3.2:latest",
		"messages": [{
			"role": "developer",
			"content": (
				"You are a strict critic. Given the following question, determine if the answer a full anwser to the question.\n\n"
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
