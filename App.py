import streamlit as st
import asyncio
import os
from openai import AsyncAzureOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
import opik
from Configure import Config

# Configure Opik for local setup
opik.configure(url="http://localhost:5173/api")

# Page configuration
st.set_page_config(
    page_title="OpenAI Agents with Opik Tracing",
    page_icon="ðŸ¤–",
    layout="wide"
)

class OpenAIAgentApp:
    def __init__(self):
        self.config = Config()
        self.setup_opik()

    def setup_opik(self):
        """Initialize Opik tracing"""
        try:
            # Create Opik client for local setup
            self.opik_client = opik.Opik(url="http://localhost:5173/api")
            st.success("Opik tracing initialized successfully!")
        except Exception as e:
            st.warning(f"Opik not available: {e}")
            self.opik_client = None

    def create_azure_client(self):
        """Create Azure OpenAI client"""
        return AsyncAzureOpenAI(
            api_key=self.config.AZURE_OPENAI_KEY,
            api_version=self.config.AZURE_API_VERSION,
            azure_endpoint=self.config.AZURE_OPENAI_ENDPOINT
        )

    def create_agent(self, azure_client):
        """Create OpenAI agent with Azure client"""
        return Agent(
            name="Azure Assistant",
            instructions="""You are a helpful AI assistant powered by Azure OpenAI. 
            Provide clear, accurate, and helpful responses to user queries.""",
            model=OpenAIChatCompletionsModel(
                model=self.config.AZURE_DEPLOYMENT_NAME,
                openai_client=azure_client
            )
        )

    @opik.track()
    async def process_query(self, query: str, agent: Agent):
        """Process user query with Opik tracing"""
        try:
            result = await Runner.run(agent, query)
            return result.final_output
        except Exception as e:
            return f"Error processing query: {str(e)}"

    def run_query_sync(self, query: str):
        """Synchronous wrapper for async query processing"""
        try:
            azure_client = self.create_azure_client()
            agent = self.create_agent(azure_client)

            # Run async function in sync context
            return asyncio.run(self.process_query(query, agent))
        except Exception as e:
            return f"Error: {str(e)}"

def main():
    st.title("OpenAI Agents SDK with Azure & Opik Tracing")
    st.markdown("---")

    # Initialize app
    if 'agent_app' not in st.session_state:
        st.session_state.agent_app = OpenAIAgentApp()

    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        st.info("Make sure to set your Azure OpenAI credentials in the .env file")

        # Display configuration status
        config = Config()
        if config.AZURE_OPENAI_KEY and config.AZURE_OPENAI_ENDPOINT:
            st.success("Azure OpenAI configured")
        else:
            st.error("Azure OpenAI not configured")

        st.header("Tracing")
        st.info("Visit http://localhost:5173 to view Opik dashboard")

        if st.button("Reset Conversation"):
            st.session_state.messages = []
            st.rerun()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.agent_app.run_query_sync(prompt)
                st.markdown(response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Footer
    st.markdown("---")
    st.markdown("Built with OpenAI Agents SDK, Azure OpenAI, and Opik tracing")

if __name__ == "__main__":
    main()