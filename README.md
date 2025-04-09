# Daytona Sandbox Orchestration Agent

An agent that orchestrates Daytona sandbox environments and communicates with other agents using the Agent-to-Agent (A2A) protocol.

## Overview

This agent manages the lifecycle of Daytona sandbox environments, including creation, configuration, and deletion. It can communicate with other agents, such as the coder agent, to coordinate development activities.

## Features

- Create and manage Daytona sandbox environments
- Communicate with other agents using the A2A protocol
- Provide templates for common development environments
- Configure sandboxes based on development requirements

## Installation

```bash
# Clone the repository
git clone https://github.com/nkkko/dagent.git
cd dagent

# Install the package
pip install -e .
```

## Setup

1. Create a virtual environment and activate it:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

2. Install the package and dependencies:
   ```bash
   pip install -e .
   ```

3. Set up environment variables by copying the example file and filling in your API keys:
   ```bash
   cp .env.example .env
   ```

4. Edit the `.env` file and add your API keys:
   ```
   # Daytona API Configuration
   DAYTONA_API_KEY=your_daytona_api_key_here
   DAYTONA_API_URL=https://app.daytona.io/api
   DAYTONA_API_TARGET=us

   # A2A Configuration
   A2A_HOST_URL=http://localhost:8080

   # LLM Configuration
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Running the Agent

### Method 1: Using the run script (recommended)

Run the agent with environment variables from `.env`:
```bash
python run.py
```

### Method 2: Using the module directly

Run with environment variables from `.env`:
```bash
python -m src.main
```

Or run with custom settings:
```bash
python -m src.main --host-url http://a2a-host:8080 --api-url https://app.daytona.io/api --api-key your-daytona-key --gemini-key your-gemini-key --verbose
```

## Running Examples

The `examples/` directory contains sample code for working with the agent:

- `examples/coder_communication.py`: Demonstrates basic communication with the coder agent
- `examples/coder_workflow.py`: Simulates a complete workflow between agents
- `examples/use_env_config.py`: Shows how to use environment variables with the agent

Run an example:
```bash
python -m examples.use_env_config
```

## Interacting with the Agent

Once running, the agent will listen for connections in the terminal window. The agent will log information about its configuration and any operations it performs.

To interrupt the agent, press Ctrl+C in the terminal window.

## Troubleshooting

- If you encounter module-related errors, make sure you've installed the package with `pip install -e .`
- If the code complains about missing classes or methods, it may be due to version differences in the ADK Python SDK
- For API keys, make sure they're properly set in your `.env` file or passed as command-line arguments
- For more verbose logging, use the `--verbose` flag

## Communication with Coder Agent

The Daytona Sandbox Orchestration Agent can communicate with the coder agent defined in `/dagent/A2A/samples/js/src/agents/coder`. This allows for coordinated development activities, where:

1. The coder agent can request a development environment
2. The Daytona agent creates and configures the environment
3. The coder agent performs development tasks in the environment
4. The Daytona agent manages the environment lifecycle

Example communication flow:

```
Coder Agent: "I need a Python development environment for a Django project"
Daytona Agent: *creates sandbox with Python template*
Daytona Agent: "Created sandbox-123. URL: https://sandbox-123.example.com"
Coder Agent: *performs development tasks*
Coder Agent: "I'm done with the development environment"
Daytona Agent: *deletes sandbox*
```

## Development

### Project Structure

```
dagent/
├── SPECS.md          # Specification document
├── README.md         # This README
├── setup.py          # Package setup
├── .env.example      # Example environment variables
├── examples/         # Example usage scripts
└── src/
    ├── main.py       # Main application
    ├── config.py     # Configuration
    └── agent/
        ├── __init__.py
        ├── daytona_agent.py  # Agent implementation
        ├── a2a_integration.py  # A2A protocol integration
        └── tools.py  # Daytona-specific tools
```

### Prerequisites

- Python 3.8 or higher
- Access to the Google ADK Python SDK
- Access to the A2A protocol implementation
- Daytona API key (get one from https://app.daytona.io/)
- Gemini API key

## License

[MIT License](LICENSE)