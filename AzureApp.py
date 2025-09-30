import os
import asyncio
import streamlit as st
from openai import AsyncAzureOpenAI
from agents import Agent, Runner
from agents.models import OpenAIChatCompletionsModel
import opik
from opik.integrations.openai import track_openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIAgentApp:
    def __init__(self):
        self.opik_client = None
        self.azure_client = None
        self.agent = None
        self.setup_clients()
        self.setup_agent()

    def setup_clients(self):
        """Initialize Azure OpenAI and Opik clients"""
        try:
            # Initialize Opik client
            self.opik_client = opik.Opik(
                project_name=os.getenv("OPIK_PROJECT_NAME", "azure-openai-agents"),
                workspace=os.getenv("OPIK_WORKSPACE")
            )

            # Initialize Azure OpenAI client
            self.azure_client = AsyncAzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            )

            # Track Azure OpenAI calls with Opik
            self.azure_client = track_openai(
                self.azure_client,
                project_name=os.getenv("OPIK_PROJECT_NAME", "azure-openai-agents")
            )

            st.success("Clients initialized successfully!")

        except Exception as e:
            st.error(f"Error initializing clients: {str(e)}")
            return False

        return True

    def setup_agent(self):
        """Create and configure the AI agent"""
        try:
            self.agent = Agent(
                name="Azure AI Assistant",
                instructions="""
                You are a helpful AI assistant running on Azure OpenAI.

                Guidelines:
                - Provide clear, helpful, and accurate responses
                - Be conversational and friendly
                - If you're unsure about something, say so
                - Keep responses concise but informative
                - You can help with various tasks like answering questions, 
                  providing explanations, writing assistance, and problem-solving
                """,
                model=OpenAIChatCompletionsModel(
                    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini"),
                    openai_client=self.azure_client,
                ),
            )
            st.success("AI Agent configured successfully!")

        except Exception as e:
            st.error(f"Error setting up agent: {str(e)}")
            return False

        return True

    @opik.track(name="agent_conversation")
    async def process_message(self, user_input: str) -> str:
        """Process user message through the AI agent with Opik tracing"""
        try:
            # Use Opik to track the conversation
            with opik.track_context():
                # Run the agent with user input
                result = await Runner.run(
                    agent=self.agent,
                    input=user_input
                )

                # Log the interaction to Opik
                opik.log_traces([{
                    "name": "azure_agent_response",
                    "input": {"user_message": user_input},
                    "output": {"agent_response": result.final_output},
                    "metadata": {
                        "model": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini"),
                        "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
                        "agent_name": self.agent.name
                    }
                }])

                return result.final_output

        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            st.error(f"{error_msg}")
            return error_msg


def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Azure OpenAI Agents with Opik",
        page_icon="ðŸ¤–",
        layout="wide"
    )

    st.title("ðŸ¤– Azure OpenAI Agent with Opik Tracing")
    st.markdown("A simple AI agent using OpenAI Agents SDK on Azure with Opik observability")

    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        st.markdown("Required Environment Variables:")

        env_vars = [
            ("AZURE_OPENAI_API_KEY", "Your Azure OpenAI API key"),
            ("AZURE_OPENAI_ENDPOINT", "Azure OpenAI endpoint URL"),
            ("AZURE_OPENAI_DEPLOYMENT_NAME", "Model deployment name"),
            ("OPIK_API_TOKEN", "Opik API token (optional for local)"),
            ("OPIK_PROJECT_NAME", "Opik project name"),
            ("OPIK_WORKSPACE", "Opik workspace name")
        ]

        for var_name, description in env_vars:
            value = os.getenv(var_name, "Not set")
            if value == "Not set":
                st.error(f"âŒ {var_name}: {value}")
            else:
                st.success(f"âœ… {var_name}: {'*' * min(len(value), 10)}...")
            st.caption(description)

        st.markdown("---")
        st.markdown("Opik Dashboard")
        st.markdown("[View Traces & Analytics](https://www.comet.com/opik)")

    # Initialize the app
    if 'app' not in st.session_state:
        with st.spinner("Initializing AI Agent..."):
            st.session_state.app = AIAgentApp()

    # Check if agent is ready
    if st.session_state.app.agent is None:
        st.error("AI Agent is not properly initialized. Please check your environment variables.")
        st.stop()

    # Chat interface
    st.header("Chat with AI Agent")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Hello! I'm your Azure AI Assistant with Opik tracing. How can I help you today?"
        })

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Process message through the agent
                    response = asyncio.run(st.session_state.app.process_message(prompt))
                    st.markdown(response)

                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})

                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Hello! I'm your Azure AI Assistant with Opik tracing. How can I help you today?"
        })
        st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("""
    **About this app:**
    - Uses OpenAI Agents SDK for agent management
    - Connects to Azure OpenAI for LLM processing
    - Integrated with Opik for comprehensive tracing and telemetry
    - Built with Streamlit for simple UI
    """)


if __name__ == "__main__":
    main()