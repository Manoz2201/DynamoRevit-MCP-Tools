# Model Context Protocol (MCP) for Dynamo and Revit

This repository contains a collection of tools and automations built on the **Model Context Protocol (MCP)**. The goal of MCP is to create a robust and reusable framework for interacting with software APIs, with an initial focus on Autodesk Revit and Dynamo.

## What is MCP?

The "Model Context Protocol" (MCP) is a framework for creating powerful, context-aware automation tools. An "MCP Tool" is a self-contained component that performs a specific task by interacting with one or more APIs, guided by these key principles:

1.  **Context-Awareness**: Tools understand the environment they run in (e.g., the current Revit model, user selections).
2.  **Modularity**: Tools are small, focused, and can be combined to create complex workflows.
3.  **API Abstraction**: Tools provide simple interfaces that hide the complexity of underlying APIs like the Revit API.
4.  **Robustness**: Tools include strong error handling and clear logging.

## Automation Tools

This repository will house various MCP tools. Our initial focus is on automating Dynamo via its command-line interface.

### Planned Tools:

*   **`RunDynamoGraph`**: Executes a `.dyn` file in a headless mode, perfect for batch processing and integration into larger scripts.
*   **`ExecuteDynamoCommands`**: Runs a series of commands from a file for more complex, multi-step automations.
*   **`ConvertDynamoFile`**: A utility for upgrading Dynamo graphs to the latest file format.

## Getting Started

*(This section will be updated as tools are developed.)* 