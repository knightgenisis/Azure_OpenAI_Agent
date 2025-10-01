"""
Demonstration script showing Opik integration with Azure OpenAI Agents
This script shows how tracing works and generates sample data for the dashboard
"""

import os
import asyncio
import time
from datetime import datetime
from openai import AsyncAzureOpenAI
from agents import Agent, Runner
from agents.models import OpenAIChatCompletionsModel
import opik
from opik.integrations.openai import track_openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OpikDemoAgent:
    def __init__(self):
        self.setup_clients()
        self.setup_agent()

    def setup_clients(self):
        """Initialize clients with detailed logging"""
        print("Setting up Azure OpenAI and Opik clients...")

        # Initialize Opik client with project details
        self.opik_client = opik.Opik(
            project_name=os.getenv("OPIK_PROJECT_NAME", "azure-openai-demo"),
            workspace=os.getenv("OPIK_WORKSPACE")
        )
        print(f"Opik client initialized for project: {os.getenv('OPIK_PROJECT_NAME', 'azure-openai-demo')}")

        # Initialize Azure OpenAI
        self.azure_client = AsyncAzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        )

        # Enable Opik tracking for all Azure OpenAI calls
        self.azure_client = track_openai(
            self.azure_client,
            project_name=os.getenv("OPIK_PROJECT_NAME", "azure-openai-demo")
        )
        print("Azure OpenAI client initialized with Opik tracking")

    def setup_agent(self):
        """Create AI agent with specific instructions"""
        self.agent = Agent(
            name="Demo AI Assistant",
            instructions="""
            You are a knowledgeable AI assistant for a demonstration.

            Your role:
            - Provide helpful and informative responses
            - Be engaging and conversational
            - Include relevant details and examples
            - Maintain a friendly, professional tone

            This is a demo showing AI agent capabilities with Azure OpenAI and Opik tracing.
            """,
            model=OpenAIChatCompletionsModel(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini"),
                openai_client=self.azure_client,
            ),
        )
        print("AI Agent configured successfully")

    @opik.track(
        name="demo_conversation",
        tags=["demo", "azure-openai", "agents"]
    )
    async def process_with_tracing(self, user_input: str, conversation_id: str = None):
        """Process message with comprehensive Opik tracing"""

        start_time = time.time()

        try:
            # Create trace with metadata
            with opik.track_context():
                # Log input details
                opik.log_traces([{
                    "name": "user_input_received",
                    "input": {"message": user_input},
                    "metadata": {
                        "timestamp": datetime.now().isoformat(),
                        "conversation_id": conversation_id,
                        "model": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini"),
                        "agent_name": self.agent.name
                    }
                }])

                print(f"Processing: '{user_input[:50]}{'...' if len(user_input) > 50 else ''}'")

                # Run the agent
                result = await Runner.run(
                    agent=self.agent,
                    input=user_input
                )

                processing_time = time.time() - start_time

                # Log the complete interaction
                opik.log_traces([{
                    "name": "agent_response_generated",
                    "input": {"user_message": user_input},
                    "output": {
                        "agent_response": result.final_output,
                        "processing_time_seconds": processing_time
                    },
                    "metadata": {
                        "timestamp": datetime.now().isoformat(),
                        "conversation_id": conversation_id,
                        "model": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini"),
                        "agent_name": self.agent.name,
                        "success": True,
                        "response_length": len(result.final_output),
                        "processing_time": f"{processing_time:.2f}s"
                    },
                    "tags": ["successful_response", "demo"]
                }])

                print(f"Response generated in {processing_time:.2f}s")
                return result.final_output

        except Exception as e:
            processing_time = time.time() - start_time

            # Log error with Opik
            opik.log_traces([{
                "name": "agent_error",
                "input": {"user_message": user_input},
                "output": {"error": str(e)},
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "conversation_id": conversation_id,
                    "error_type": type(e).__name__,
                    "processing_time": f"{processing_time:.2f}s",
                    "success": False
                },
                "tags": ["error", "demo"]
            }])

            print(f"Error after {processing_time:.2f}s: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"

async def run_demo():
    """Run a comprehensive demo showing Opik integration"""

    print("\n" + "="*60)
    print("AZURE OPENAI AGENT + OPIK TRACING DEMO")
    print("="*60)

    # Initialize the demo agent
    demo = OpikDemoAgent()

    # Demo conversation scenarios
    demo_conversations = [
        {
            "id": "conv_001",
            "messages": [
                "Hello! Can you explain what artificial intelligence is?",
                "What are the main applications of AI in business today?",
                "How does machine learning differ from traditional programming?"
            ]
        },
        {
            "id": "conv_002", 
            "messages": [
                "What is cloud computing and why is it important?",
                "Can you explain the benefits of using Azure services?",
                "How does serverless computing work?"
            ]
        },
        {
            "id": "conv_003",
            "messages": [
                "What are the best practices for software development?",
                "Explain the concept of DevOps and its benefits",
                "What is continuous integration and deployment?"
            ]
        }
    ]

    print(f"\nRunning {len(demo_conversations)} demo conversations...")
    print("All interactions will be tracked in Opik for analysis")
    print("-" * 60)

    total_interactions = 0

    for conv in demo_conversations:
        conv_id = conv["id"]
        messages = conv["messages"]

        print(f"\nStarting Conversation {conv_id}")
        print(f"{len(messages)} messages to process")

        for i, message in enumerate(messages, 1):
            print(f"\n{len(messages)}] User: {message}")

            response = await demo.process_with_tracing(
                user_input=message,
                conversation_id=conv_id
            )

            print(f"Assistant: {response[:100]}{'...' if len(response) > 100 else ''}")
            total_interactions += 1

            # Small delay to make demo more realistic
            await asyncio.sleep(1)

        print(f"Conversation {conv_id} completed")

    print("\n" + "="*60)
    print(f"DEMO COMPLETED!")
    print(f"Total interactions processed: {total_interactions}")
    print(f"Project name: {os.getenv('OPIK_PROJECT_NAME', 'azure-openai-demo')}")
    print("\nVIEW YOUR DATA IN OPIK:")
    print("Dashboard: https://www.comet.com/opik")
    print("Check traces, response times, and analytics")
    print("Filter by tags: 'demo', 'successful_response', 'error'")
    print("Analyze conversation patterns and performance")
    print("="*60)

def print_opik_analytics_guide():
    """Print guide for analyzing data in Opik dashboard"""
    print("\nOPIK ANALYTICS GUIDE:")
    print("-" * 30)
    print("\nWhat to look for in your Opik dashboard:")
    print("\n1.TRACES TAB:")
    print("View all conversation traces")
    print("Check response times and token usage")
    print("Filter by conversation_id, tags, or time range")
    print("\n2.ANALYTICS TAB:")
    print("Response time trends")
    print("Token usage and cost analysis") 
    print("Success/error rates")
    print("\n3.FILTERING & SEARCH:")
    print(" Use tags: 'demo', 'successful_response'")
    print("Search by conversation_id (e.g., 'conv_001')")
    print("Filter by date range or model type")
    print("\n4.TRACE DETAILS:")
    print("Click any trace to see full conversation")
    print("View input/output, metadata, and timings")
    print("Analyze error traces for debugging")

async def main():
    """Main demo function"""

    # Check if environment is set up
    required_vars = ["AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_DEPLOYMENT_NAME"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print("Missing required environment variables:")
        for var in missing_vars:
            print(f"{var}")
        print("\nPlease set these in your .env file and try again.")
        return

    # Run the demo
    try:
        await run_demo()
        print_opik_analytics_guide()

    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\nDemo failed with error: {str(e)}")
        print("Please check your configuration and try again")

if __name__ == "__main__":
    asyncio.run(main())