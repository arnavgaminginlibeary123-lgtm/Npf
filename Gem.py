import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI # New Import
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferMemory
from langchain import hub

class ArnavAI:
    def __init__(self):
        # 1. Use the new Google Key from Secrets
        google_key = st.secrets["GOOGLE_API_KEY"]
        tavily_key = st.secrets["TAVILY_API_KEY"]
        
        # 2. Setup Gemini (FREE TIER)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", 
            google_api_key=google_key,
            temperature=0.3
        )
        
        os.environ["TAVILY_API_KEY"] = tavily_key
        self.search = TavilySearchResults(k=3)
        self.tools = [self.search]

        if "memory" not in st.session_state:
            st.session_state.memory = ConversationBufferMemory(
                memory_key="chat_history", 
                return_messages=True
            )

        # 3. Pull a compatible prompt
        prompt = hub.pull("hwchase17/openai-tools-agent")
        
        # 4. Build the Agent
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        self.executor = AgentExecutor(
            agent=agent, 
            tools=self.tools, 
            memory=st.session_state.memory, 
            verbose=True,
            handle_parsing_errors=True
        )

    def get_response(self, user_input):
        try:
            return self.executor.invoke({"input": user_input})["output"]
        except Exception as e:
            return f"Arnav AI 3.0 (Gemini Edition) Error: {str(e)}"

