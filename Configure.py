import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration management for Azure OpenAI and Opik"""
    
    # Azure OpenAI Settings
    AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o')
    AZURE_API_VERSION = os.getenv('AZURE_API_VERSION', '2024-02-01')
    
    # Opik Settings (local setup)
    OPIK_PROJECT_NAME = os.getenv('OPIK_PROJECT_NAME', 'Azure-OpenAI-Agent')
    
    @classmethod
    def validate_config(cls):
        """Validate required configuration"""
        missing = []
        if not cls.AZURE_OPENAI_API_KEY:
            missing.append('AZURE_OPENAI_API_KEY')
        if not cls.AZURE_OPENAI_ENDPOINT:
            missing.append('AZURE_OPENAI_ENDPOINT')
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        return True
    
    @classmethod
    def get_status(cls):
        """Get configuration status for display"""
        return {
            'configured': bool(cls.AZURE_OPENAI_API_KEY and cls.AZURE_OPENAI_ENDPOINT),
            'endpoint': cls.AZURE_OPENAI_ENDPOINT,
            'deployment': cls.AZURE_OPENAI_DEPLOYMENT,
            'project': cls.OPIK_PROJECT_NAME
        }

# Test configuration when run directly
if __name__ == "__main__":
    print("ðŸ”§ Configuration Test")
    print("-" * 30)
    
    status = Config.get_status()
    print(f"Configured: {'âœ…' if status['configured'] else 'âŒ'}")
    print(f"Endpoint: {status['endpoint'] or 'Not set'}")
    print(f"Deployment: {status['deployment']}")
    print(f"Opik Project: {status['project']}")
    
    if status['configured']:
        print("\nâœ… Ready to go!")
    else:
        print("\nâŒ Please set up your .env file with Azure OpenAI credentials")