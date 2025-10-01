# OpenAI Agents SDK with Azure OpenAI & Opik Tracing

A production-ready Python application that demonstrates how to build AI agents using the OpenAI Agents SDK with Azure OpenAI, featuring a Streamlit web interface and local Opik tracing for monitoring and observability.

## Features

- **OpenAI Agents SDK**: Build sophisticated AI agents with the official SDK
- **Azure OpenAI Integration**: Use Azure-hosted OpenAI models 
- **Streamlit Web UI**: Clean, interactive chat interface
- **Opik Tracing**: Local observability and tracing for agent interactions
- **Docker Support**: Full containerization for easy deployment
- **Team Collaboration**: GitHub-ready with proper configuration management

## Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Azure OpenAI resource with deployed model
- Git (for version control)

## Quick Setup

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/openai-agents-opik-app.git
cd openai-agents-opik-app

# Copy environment template
copy Credentials.example .env
```

### 2. Configure Environment

Edit `.env` with your Azure OpenAI credentials:

```bash
AZURE_OPENAI_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_DEPLOYMENT_NAME=gpt-4o
```

### 3. Run with Docker Compose (Recommended)

```bash
# Start all services (app + Opik)
docker-compose up --build

# Access the app at: http://localhost:8501
# Access Opik dashboard at: http://localhost:5173
```

### 4. Alternative: Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Opik separately (in another terminal)
git clone https://github.com/comet-ml/opik.git
cd opik
docker-compose -f deployment/docker-compose/docker-compose.yaml up -d

# Run the Streamlit app
cd ../openai-agents-opik-app
streamlit run app.py
```

## ðŸ—ï¸ Project Structure

```
openai-agents-opik-app/
 app.py                  # Main Streamlit application
 config.py              # Configuration management
 requirements.txt        # Python dependencies
 Dockerfile             # Container configuration
 docker-compose.yml     # Multi-service orchestration
 Credentials.example           # Environment variables template
 .gitignore            # Git ignore rules
 README.md             # This file
```

## How It Works

### Application Flow

1. **User Input**: User enters a query in the Streamlit chat interface
2. **Agent Processing**: OpenAI Agents SDK processes the query using Azure OpenAI
3. **Tracing**: Opik automatically captures and traces the interaction
4. **Response**: The agent's response is displayed in the chat interface
5. **Monitoring**: View detailed traces and metrics in the Opik dashboard

### Key Components

- **`app.py`**: Main Streamlit application with chat interface
- **`config.py`**: Environment-based configuration management
- **OpenAI Agents SDK**: Handles agent creation and query processing
- **Opik Integration**: Automatic tracing with `@opik.track()` decorator
- **Azure OpenAI**: Cloud-hosted model inference

## Docker Deployment

### Production Deployment

```bash
# Build and run in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f openai-agents-app

# Stop services
docker-compose down
```

### Development Mode

```bash
# Run with volume mounting for live code changes
docker-compose -f docker-compose.yml up --build
```

## Monitoring with Opik

1. **Access Dashboard**: Navigate to http://localhost:5173
2. **View Traces**: See real-time agent interactions and performance
3. **Analyze Metrics**: Monitor response times, token usage, and success rates
4. **Debug Issues**: Detailed trace information for troubleshooting

## Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AZURE_OPENAI_KEY` | Azure OpenAI API key | Required |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | Required |
| `AZURE_DEPLOYMENT_NAME` | Model deployment name | gpt-4o |
| `AZURE_API_VERSION` | Azure OpenAI API version | 2024-02-01 |
| `OPIK_URL` | Opik instance URL | http://localhost:5173/api |
| `STREAMLIT_SERVER_PORT` | Streamlit port | 8501 |

### Customization

- **Agent Instructions**: Modify the agent's behavior in `app.py`
- **UI Styling**: Customize Streamlit interface appearance
- **Tracing Options**: Configure Opik tracing granularity
- **Model Parameters**: Adjust temperature, max_tokens, etc.

## Team Collaboration

### Git Workflow

```bash
# Clone repository
git clone https://github.com/yourusername/openai-agents-opik-app.git

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "Add your feature"

# Push and create pull request
git push origin feature/your-feature-name
```

### Development Best Practices

1. **Environment**: Always use `.env` for local development
2. **Dependencies**: Update `requirements.txt` when adding packages
3. **Testing**: Test changes locally before committing
4. **Documentation**: Update README.md for significant changes

## ðŸš¨ Troubleshooting

### Common Issues

**Azure OpenAI Connection Failed**
- Verify your API key and endpoint in `.env`
- Check that your Azure OpenAI resource is active
- Ensure the deployment name matches your Azure configuration

**Opik Not Available**
- Make sure Docker is running
- Check if Opik services are healthy: `docker-compose ps`
- Restart Opik services: `docker-compose restart opik-backend opik-frontend`

**Port Conflicts**
- Change ports in `docker-compose.yml` if 8501 or 5173 are in use
- Update environment variables accordingly

### Logs and Debugging

```bash
# View application logs
docker-compose logs -f openai-agents-app

# View Opik logs
docker-compose logs -f opik-backend

# Check service status
docker-compose ps
```

## ðŸ“ˆ Performance Tips

1. **Model Selection**: Use appropriate Azure OpenAI model for your use case
2. **Caching**: Implement response caching for repeated queries
3. **Async Processing**: The app uses async processing for better performance
4. **Resource Limits**: Configure Docker resource limits in production

## ðŸ” Security Considerations

1. **Environment Variables**: Never commit `.env` to version control
2. **API Keys**: Rotate keys regularly
3. **Network Security**: Use HTTPS in production
4. **Container Security**: Run containers as non-root user (configured in Dockerfile)

## ðŸ“š Additional Resources

- [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)
- [Azure OpenAI Service Documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/openai/)
- [Opik Documentation](https://github.com/comet-ml/opik)
- [Streamlit Documentation](https://docs.streamlit.io/)

## ðŸ¤ Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## ðŸ“„ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ðŸ™‹â€â™‚ï¸ Support

- Create an issue for bugs or feature requests
- Check existing issues before creating new ones
- Provide detailed information for troubleshooting

---

**Happy coding! ðŸš€**