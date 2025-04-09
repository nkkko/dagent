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

## Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
# Daytona API Configuration
DAYTONA_API_KEY=your_daytona_api_key_here
DAYTONA_API_URL=https://app.daytona.io/api
DAYTONA_API_TARGET=us

# A2A Configuration
A2A_HOST_URL=http://localhost:8080
```

You can copy the `.env.example` file and update it with your credentials:

```bash
cp .env.example .env
# Edit .env with your API keys
```

## Usage

### Running the Agent

```bash
# Run with environment variables from .env
python run.py

# Run with custom settings via command line
python -m src.main --host-url http://a2a-host:8080 --api-url http://daytona-api:8090 --api-key your-api-key --verbose
```

### Example Usage

The `examples/` directory contains sample code for working with the agent:

- `examples/coder_communication.py`: Demonstrates basic communication with the coder agent
- `examples/coder_workflow.py`: Simulates a complete workflow between agents
- `examples/use_env_config.py`: Shows how to use environment variables with the agent

Run an example:

```bash
python -m examples.use_env_config
```

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

## License

[MIT License](LICENSE)