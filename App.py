import os
import uuid
import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI
import opik
from opik.integrations.openai import track_openai
from opik import track

# 1️⃣ Load environment variables first
load_dotenv()

# 2️⃣ Configure Opik (use cloud if local not running)
opik.configure(
    api_key=os.getenv("OPIK_API_KEY"),
    workspace=os.getenv("OPIK_WORKSPACE"),
    use_local=False  # Set True only if running a local Opik server
)

# 3️⃣ Initialize Azure OpenAI client with tracing
azure_client = AzureOpenAI(
    api_version=os.getenv("OPENAI_API_VERSION")
)
client = track_openai(azure_client)

# 4️⃣ Streamlit UI setup...
st.set_page_config(page_title="Azure AI Agent with Opik Tracing", page_icon="🤖", layout="centered")
st.title("🤖 Azure AI Agent with Real-time Tracing")
st.caption("Built using Streamlit, Azure OpenAI, and Opik by Comet ML")
st.sidebar.success("✅ Opik Tracing Active")

# 5️⃣ Session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a professional AI assistant."}]

# Initialize thread_id for conversation tracking
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# 6️⃣ Display chat history
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 7️⃣ Chat input and response
@track(name="generate_response", tags=["chat", "azure-openai"])
def generate_response(prompt: str, messages: list):
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        messages=messages,
        temperature=0.7,
        opik_args={"trace": {"thread_id": st.session_state.thread_id}}
    )
    return response.choices[0].message.content

if prompt := st.chat_input("Ask the AI agent anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                reply = generate_response(
                    prompt,
                    [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                )
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error communicating with Azure OpenAI: {e}")
