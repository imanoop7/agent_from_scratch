"""Basic chat completion example using the Ollama client shim."""

from src.utils.ai import openai


def main():
	# Ask the model for a simple name-style response
	completion = openai.chat.completions.create({
		"messages": [
			{"role": "developer", "content": "You are a helpful assistant, if asked your name say Hello World."},
			{"role": "user", "content": "What is your name?"},
		],
		"model": "llama3.2:latest",
	})
	print(completion.get("choices", [None])[0])


if __name__ == "__main__":
	main()
