# Agent From Scratch

## Overview

Agent From Scratch is a project designed to build a functional and modular AI agent using custom Python modules. The project demonstrates a comprehensive approach to developing autonomous agents, starting from core AI functionalities to advanced planning and tool usage.

## Project Structure

- **ai.py**: Main logic for the agent.
- **browse_web.py**: Module for web browsing capabilities.
- **index.py**: Entry point for initializing the agent.
- **llm_judge.py**: Leverages language models for decision-making.
- **step0_llm.py**: Initial integration of the large language model component.
- **step1_condition.py**: Contains conditional logic crucial for the agent's decision processes.
- **step2_tool.py**: Integrates various tools that enhance the capabilities of the agent.
- **step3_refactor.py**: Contains scripts aimed at refactoring and optimizing the code.
- **step4_planning.py**: Implements planning and structured workflow organization.
- **todo_list.py**: Manages the agent’s todo list and progress tracking.

## Features

- **Modular Design**: The project is divided into logical, independent modules that can be extended or modified as needed.
- **Language Model Integration**: Utilizes advanced language models for intelligent decision making and planning.
- **Tool Integration**: Demonstrates how to interface with a diverse set of tools for web browsing, refactoring, and more.
- **Scalability and Maintenance**: Built with scalability in mind, emphasizing best practices and maintainability.

## Getting Started

### Prerequisites

- Python 3.8 or later
- Required packages listed in `requirements.txt`
- Ollama running locally (for the OpenAI-compatible API at `http://localhost:11434/v1`)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/imanoop7/agent_from_scratch.git
   ```
2. Navigate into the project directory:
   ```bash
   cd agent_from_scratch
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Single-Agent Quickstart (Windows PowerShell)

1) Create and activate a virtual environment, then install dependencies:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

2) Install and start Ollama (one-time):

- Download and install from https://ollama.com/download
- Start Ollama (it runs a local server on port 11434).
- Pull a model (default in this repo is `llama3.2:latest`):

```powershell
ollama pull llama3.2
```

3) Run a single agent with planning and tools:

```powershell
python .\run_agent.py --goal "I want to learn about building agents without a framework."
```

Notes:
- If your Ollama server is on a different host/port, set `OLLAMA_BASE_URL` (e.g. `http://myhost:11434/v1`).
- To change the model: `--model llama3.1:8b` (or whatever you've pulled in Ollama).

### Alternative demo scripts

- `step0_llm.py`: Minimal single completion.
- `step1_condition.py`: Two-call pattern (answer, then judge).
- `step3_refactor.py`: Tool loop using the shared registry.
- `step4_planning.py`: Planning-first flow similar to `run_agent.py`.

## Contributing

Contributions are welcome! Please ensure that any changes follow the project's coding standards and that all tests pass prior to submission.

## License

This project is licensed under the MIT License.

## Contact

For any questions or further information, please contact the project maintainer.

