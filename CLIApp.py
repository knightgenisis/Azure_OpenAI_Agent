import os
import asyncio
from openai import AsyncAzureOpenAI
from agents import Agent, Runner
from agents.models import OpenAIChatCompletionsModel
import opik
from opik.integrations.openai import track_openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SimpleAIAgent:
    def __init__(self):
        self.opik_client = None
        self.azure_client = None
        self.agent = None
        self.setup_clients()
        self.setup_agent()

    def setup_clients(self):
        """Initialize Azure OpenAI and Opik clients"""
        try:
            print("Initializing clients...")

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

            print("Clients initialized successfully!")

        except Exception as e:
            print(f"Error initializing clients: {str(e)}")
            return False

        return True

    def setup_agent(self):
        """Create and configure the AI agent"""
        try:
            print("Setting up AI agent...")

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
            print("AI Agent configured successfully!")

        except Exception as e:
            print(f"Error setting up agent: {str(e)}")
            return False

        return True

    @opik.track(name="agent_conversation")
    async def process_message(self, user_input: str) -> str:
        """Process user message through the AI agent with Opik tracing"""
        try:
            print("Processing your message...")

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
            print(f"{error_msg}")
            return error_msg

    async def run_chat(self):
        """Run the interactive chat loop"""
        print("\n" + "="*60)
        print("ðŸ¤– Azure OpenAI Agent with Opik Tracing")
        print("="*60)
        print("Type 'quit', 'exit', or 'bye' to end the conversation")
        print("Your messages are being traced with Opik for observability")
        print("="*60 + "\n")

        if self.agent is None:
            print("Agent is not properly initialized. Please check your environment variables.")
            return

        while True:
            try:
                # Get user input
                user_input = input("\nYou: ").strip()

                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'q', 0]:
                    print("\nGoodbye! Check your Opik dashboard for conversation traces.")
                    break

                if not user_input:
                    print("Please enter a message.")
                    continue

                # Process message
                response = await self.process_message(user_input)
                print(f"\nAssistant: {response}")

            except KeyboardInterrupt:
                print("\n\nGoodbye! Check your Opik dashboard for conversation traces.")
                break
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")


def main():
    """Main function to run the CLI application"""
    # Check environment variables
    required_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_DEPLOYMENT_NAME"
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print("Missing required environment variables:")
        for var in missing_vars:
            print(f"{var}")
        print("\nPlease set these variables in your .env file or environment.")
        print("See Credentials file for reference.")
        return

    # Initialize and run the agent
    try:
        agent_app = SimpleAIAgent()
        asyncio.run(agent_app.run_chat())
    except Exception as e:
        print(f"Failed to start the application: {str(e)}")


if __name__ == "__main__":
    main()