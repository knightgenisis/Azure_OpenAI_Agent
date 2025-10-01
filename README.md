# Azure OpenAI Agent with Opik Tracing

A comprehensive Python application that demonstrates how to build AI agents using the OpenAI Agents SDK with Azure OpenAI, integrated with Opik for advanced tracing and telemetry.

## Features

- **OpenAI Agents SDK**: Simple and powerful agent framework
- **Azure OpenAI Integration**: Leverages Azure's enterprise-grade OpenAI service
- **Opik Tracing**: Comprehensive observability and analytics for AI agents
- **Dual Interface**: Both web UI (Streamlit) and command-line interface
- **Production Ready**: Built with best practices for monitoring and debugging

## Prerequisites

- Python 3.9 or higher
- Azure OpenAI resource and API key
- Opik account (free at https://www.comet.com/opik)

## Installation

1. **Clone or create the project directory:**
   ```bash
   mkdir azure-openai-agent
   cd azure-openai-agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` file with your credentials:
   ```env
   # Azure OpenAI Configuration
   AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_VERSION=2024-08-01-preview
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini

   # Opik Configuration
   OPIK_API_TOKEN=your_opik_api_token_here
   OPIK_PROJECT_NAME=azure-openai-agents
   OPIK_WORKSPACE=your_workspace_name_here
   ```

## Azure OpenAI Setup

1. **Create Azure OpenAI Resource:**
   - Go to [Azure Portal](https://portal.azure.com)
   - Create a new "Azure OpenAI" resource
   - Note down the endpoint and API key

2. **Deploy a Model:**
   - In Azure AI Foundry, go to your OpenAI resource
   - Deploy a model (e.g., `gpt-4o-mini`)
   - Note the deployment name

## Opik Setup

1. **Create Opik Account:**
   - Sign up at [Comet Opik](https://www.comet.com/opik)
   - Create a new project

2. **Get API Credentials:**
   - Go to your Opik settings
   - Copy your API token and workspace name

## Usage

### Option 1: Web Interface (Streamlit)

```bash
streamlit run azure_agent_app.py
```

This launches a user-friendly web interface where you can:
- Chat with the AI agent
- View real-time configuration status
- Access links to Opik dashboard

### Option 2: Command Line Interface

```bash
python cli_agent_app.py
```

Simple command-line chat interface with:
- Interactive conversation
- Real-time responses
- Automatic tracing to Opik

## Monitoring with Opik

Once your application is running, you can monitor it through the Opik dashboard:

1. **Visit your Opik dashboard**: https://www.comet.com/opik
2. **Select your project**: `azure-openai-agents` (or your custom name)
3. **View traces**: See all conversations, response times, and metadata
4. **Analyze performance**: Token usage, costs, and response quality

### Key Opik Features:

- **Trace Visualization**: See the complete flow of each conversation
- **Performance Metrics**: Response time, token usage, and costs
- **Error Tracking**: Identify and debug issues
- **Conversation Analytics**: Understand usage patterns
- **Custom Metadata**: Track specific business metrics



## Code Structure

- `azure_agent_app.py`: Streamlit web application
- `cli_agent_app.py`: Command-line interface
- `requirements.txt`: Python dependencies
- `.env.example`: Environment variables template
- `README.md`: This documentation

## Key Components

### 1. Agent Configuration
```python
agent = Agent(
    name="Azure AI Assistant",
    instructions="Your helpful AI assistant instructions",
    model=OpenAIChatCompletionsModel(
        model=deployment_name,
        openai_client=azure_client,
    ),
)
```

### 2. Opik Integration
```python
@opik.track(name="agent_conversation")
async def process_message(self, user_input: str) -> str:
    with opik.track_context():
        result = await Runner.run(agent=self.agent, input=user_input)
        # Automatic tracing and logging
        return result.final_output
```

### 3. Azure OpenAI Client
```python
azure_client = AsyncAzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

# Wrap with Opik tracking
azure_client = track_openai(azure_client, project_name="your-project")
```

## Troubleshooting

### Common Issues:

1. **"Resource not found" error**:
   - Verify your Azure OpenAI endpoint and deployment name
   - Ensure the model is deployed in Azure AI Foundry

2. **Opik connection issues**:
   - Check your API token and workspace name
   - Verify network connectivity to Comet servers

3. **Import errors**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Use Python 3.9 or higher

### Debug Tips:

- Check environment variables are loaded correctly
- Verify Azure OpenAI quotas and limits
- Monitor Opik dashboard for error traces
- Use CLI version for simpler debugging

## Additional Resources

- [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Opik Documentation](https://www.comet.com/docs/opik/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application.

## License

This project is open source and available under the MIT License.