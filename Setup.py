import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test if all required environment variables are set"""
    load_dotenv()

    print("Testing Environment Setup")
    print("=" * 40)

    required_vars = {
        "AZURE_OPENAI_API_KEY": "Azure OpenAI API Key",
        "AZURE_OPENAI_ENDPOINT": "Azure OpenAI Endpoint", 
        "AZURE_OPENAI_DEPLOYMENT_NAME": "Model Deployment Name",
        "OPIK_PROJECT_NAME": "Opik Project Name (optional)",
    }

    optional_vars = {
        "AZURE_OPENAI_API_VERSION": "Azure OpenAI API Version",
        "OPIK_API_TOKEN": "Opik API Token",
        "OPIK_WORKSPACE": "Opik Workspace Name"
    }

    all_good = True

    # Check required variables
    print("\nRequired Variables:")
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            print(f"{var}: {'*' * min(len(value), 8)}...")
        else:
            print(f"{var}: Not set ({description})")
            all_good = False

    # Check optional variables
    print("\nOptional Variables:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"{var}: {'*' * min(len(value), 8)}...")
        else:
            print(f"{var}: Not set ({description})")

    # Test imports
    print("\nTesting Package Imports:")
    packages = [
        ("streamlit", "Streamlit UI framework"),
        ("openai", "OpenAI Python SDK"),
        ("agents", "OpenAI Agents SDK"),
        ("opik", "Opik tracing SDK"),
        ("dotenv", "Python dotenv")
    ]

    for package, description in packages:
        try:
            __import__(package)
            print(f"{package}: Available")
        except ImportError:
            print(f"{package}: Not installed ({description})")
            all_good = False

    print("\n" + "=" * 40)
    if all_good:
        print("Environment setup looks good! You can run the application.")
        print("\nTo start:")
        print("Web UI:  streamlit run azure_agent_app.py")
        print("CLI:     python cli_agent_app.py")
    else:
        print("Please fix the issues above before running the application.")
        print("\nRefer to README.md for setup instructions.")

    return all_good

if __name__ == "__main__":
    test_environment()