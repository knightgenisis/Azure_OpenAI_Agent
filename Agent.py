import streamlit as st
from datetime import datetime
import opik
from agent import get_agent
from config import Config

# Configure Opik for local usage
opik.configure(use_local=True, project_name=Config.OPIK_PROJECT_NAME)

# Page configuration
st.set_page_config(
    page_title="Azure OpenAI Agent",
    page_icon="ðŸ¤–",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    
    .chat-container {
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "agent" not in st.session_state:
        try:
            st.session_state.agent = get_agent()
            st.session_state.agent_status = "ready"
        except Exception as e:
            st.session_state.agent = None
            st.session_state.agent_status = f"error: {str(e)}"

def display_sidebar():
    """Display sidebar with status and controls"""
    with st.sidebar:
        st.header("ðŸ”§ Status")
        
        # Configuration status
        config_status = Config.get_status()
        if config_status['configured']:
            st.markdown('<p class="status-success">âœ… Azure OpenAI Configured</p>', unsafe_allow_html=True)
            st.info(f"**Endpoint:** {config_status['endpoint']}")
            st.info(f"**Model:** {config_status['deployment']}")
        else:
            st.markdown('<p class="status-error">âŒ Azure OpenAI Not Configured</p>', unsafe_allow_html=True)
            st.error("Please check your .env file")
        
        # Agent status
        st.header("ðŸ¤– Agent")
        if st.session_state.agent_status == "ready":
            st.markdown('<p class="status-success">âœ… Agent Ready</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-error">âŒ Agent Error</p>', unsafe_allow_html=True)
            st.error(st.session_state.agent_status)
        
        # Opik status
        st.header("ðŸ“Š Opik Tracing")
        st.markdown('<p class="status-warning">ðŸ“Š Local Tracing Active</p>', unsafe_allow_html=True)
        st.info("Dashboard: http://localhost:5173\n(if Opik is running)")
        
        # Controls
        st.header("ðŸŽ›ï¸ Controls")
        
        if st.button("ðŸ”„ Test Connection", use_container_width=True):
            if st.session_state.agent:
                with st.spinner("Testing..."):
                    if st.session_state.agent.test_connection():
                        st.success("Connection works!")
                    else:
                        st.error("Connection failed!")
        
        if st.button("ðŸ—‘ï¸ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        # Stats
        if st.session_state.messages:
            st.header("ðŸ“ˆ Stats")
            total = len(st.session_state.messages)
            user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
            
            st.metric("Total Messages", total)
            st.metric("Your Messages", user_msgs)
            st.metric("Agent Responses", total - user_msgs)

@opik.track(name="streamlit_chat")
def get_response(message: str) -> str:
    """Get response from agent with Opik tracking"""
    if st.session_state.agent:
        return st.session_state.agent.chat(message)
    else:
        return "âŒ Agent not available. Please check configuration."

def main():
    """Main Streamlit application"""
    
    # Initialize session state
    init_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>ðŸ¤– Azure OpenAI Agent</h1>
        <p>Powered by OpenAI Agents SDK with Opik Tracing</p>
        <p><em>Internship Project - Team Collaboration Ready</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    display_sidebar()
    
    # Check if properly configured
    if not Config.get_status()['configured']:
        st.error("âš ï¸ **Configuration Required**")
        st.markdown("""
        **Setup Steps:**
        1. Copy `.env.example` to `.env`
        2. Add your Azure OpenAI credentials:
           ```
           AZURE_OPENAI_API_KEY=your_api_key
           AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
           AZURE_OPENAI_DEPLOYMENT=gpt-4o
           ```
        3. Restart the application
        
        See README.md for detailed instructions.
        """)
        st.stop()
    
    # Main chat interface
    st.header("ðŸ’¬ Chat with Your AI Agent")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "timestamp" in message:
                st.caption(f"â° {message['timestamp']}")
    
    # Chat input
    if prompt := st.chat_input("Type your message here...", disabled=(st.session_state.agent_status != "ready")):
        
        # Add user message
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt, 
            "timestamp": timestamp
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
            st.caption(f"â° {timestamp}")
        
        # Get and display agent response
        with st.chat_message("assistant"):
            with st.spinner("ðŸ¤” Thinking..."):
                response = get_response(prompt)
                st.markdown(response)
                response_time = datetime.now().strftime("%H:%M:%S")
                st.caption(f"â° {response_time}")
        
        # Add agent response
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response, 
            "timestamp": response_time
        })
        
        # Rerun to update UI
        st.rerun()
    
    # Welcome message for new users
    if not st.session_state.messages and st.session_state.agent_status == "ready":
        st.info("ðŸ‘‹ **Welcome!** Start chatting with your AI agent by typing a message above.")
        
        # Example prompts
        st.markdown("**Try these examples:**")
        examples = [
            "What can you help me with?",
            "Explain machine learning basics",
            "Write a Python function to sort a list",
            "What's the difference between AI and ML?"
        ]
        
        cols = st.columns(2)
        for i, example in enumerate(examples):
            with cols[i % 2]:
                if st.button(example, key=f"example_{i}", use_container_width=True):
                    # Add the example as user input
                    st.session_state.example_prompt = example
                    st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p><strong>ðŸŽ“ Internship Project</strong></p>
        <p>Built with OpenAI Agents SDK â€¢ Traced with Opik â€¢ Powered by Azure OpenAI</p>
        <p>Perfect for GitHub collaboration â€¢ No Docker required!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Optional: Setup instructions
    with st.expander("â„¹ï¸ Project Info & Setup", expanded=False):
        st.markdown("""
        ### ðŸŽ¯ Project Features
        - âœ… OpenAI Agents SDK integration
        - âœ… Azure OpenAI backend
        - âœ… Local Opik tracing (no credentials needed)
        - âœ… Streamlit web interface
        - âœ… GitHub collaboration ready
        
        ### ðŸ› ï¸ For Your Team
        - Each member creates their own `.env` file
        - Use Git branches for development
        - Never commit `.env` to version control
        - Check README.md for full setup guide
        
        ### ðŸ“Š Opik Tracing
        To enable enhanced tracing:
        1. Install: `pip install opik`
        2. Start: `opik local start`
        3. Visit: http://localhost:5173
        """)

if __name__ == "__main__":
    main()