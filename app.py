import streamlit as st
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

# ---------------- Page Config ----------------

st.set_page_config(
    page_title="GenMind AI",
    page_icon="🤖",
    layout="wide"
)

# ---------------- Initialize Session State ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- Sidebar ----------------

st.sidebar.title("GenMind AI")

st.sidebar.markdown(
"""
**Local Generative AI Assistant**

Run powerful AI models directly on your machine using Ollama.
"""
)

st.sidebar.markdown("### Features")
st.sidebar.markdown("- Local AI models")
st.sidebar.markdown("- Fast responses")
st.sidebar.markdown("- Multiple model support")

st.sidebar.markdown("### Model")

model = st.sidebar.selectbox(
    "Select Model",
    ["phi3", "llama3", "mistral"]
)

# Clear chat
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []

# ---------------- Download Chat ----------------

def export_chat():
    text = ""
    for m in st.session_state.messages:
        role = "User" if m["role"] == "user" else "Assistant"
        text += f"{role}: {m['content']}\n\n"
    return text

st.sidebar.download_button(
    "Download Chat",
    export_chat(),
    file_name="genmind_chat.txt"
)

# ---------------- Header ----------------

st.title("GenMind AI")
st.subheader("Generative AI Assistant")
st.caption("Powered by Ollama running locally")

st.divider()

# ---------------- Prompt Suggestions ----------------

col1, col2 = st.columns(2)

with col1:
    if st.button("Explain Machine Learning"):
        st.session_state.messages.append(
            {"role": "user", "content": "Explain Machine Learning"}
        )

with col2:
    if st.button("What is Generative AI?"):
        st.session_state.messages.append(
            {"role": "user", "content": "What is Generative AI?"}
        )

# ---------------- Display Chat ----------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- User Input ----------------

prompt = st.chat_input("Ask GenMind anything...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        message_placeholder = st.empty()
        full_response = ""

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": True
            },
            stream=True
        )

        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))

                if "response" in data:
                    full_response += data["response"]
                    message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )