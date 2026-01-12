import streamlit as st
from arnav_ai_chatbot import ArnavAI

# 1. Page Configuration
st.set_page_config(page_title="Arnav AI 3.0", page_icon="🤖", layout="centered")

# 2. Styling & Header
st.title("🤖 Arnav AI 3.0")
st.markdown("---")
st.sidebar.title("Settings")
st.sidebar.info("Powered by Google Gemini 1.5 Flash & Tavily Search.")

# 3. Initialize the AI Brain (Stored in session so it stays alive)
if "arnav_brain" not in st.session_state:
    st.session_state.arnav_brain = ArnavAI()

# 4. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display existing chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input Logic
if prompt := st.chat_input("Ask Arnav AI 3.0 anything..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Arnav AI is thinking..."):
            response = st.session_state.arnav_brain.get_response(prompt)
            st.markdown(response)
    
    # Add AI response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

# 7. Sidebar 'Clear Chat' Button
if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = []
    st.rerun()

