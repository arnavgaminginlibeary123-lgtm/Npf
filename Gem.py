import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch  # Official 2026 Import
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

class ArnavAI:
    def __init__(self):
        # 1. Fetch keys from Streamlit Secrets
        google_key = st.secrets["GOOGLE_API_KEY"]
        tavily_key = st.secrets["TAVILY_API_KEY"]
        
        # 2. Setup the Free Brain (Gemini 1.5 Flash)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", 
            google_api_key=google_key,
            temperature=0.3
        )
        
        # 3. Setup the Official Tavily Tool
        # os.environ is required for TavilySearch to find your key
        os.environ["TAVILY_API_KEY"] = tavily_key
        self.search_tool = TavilySearch(max_results=3)
        self.tools = [self.search_tool]

        # 4. Create the Agent
        # The modern 2026 'create_agent' handles everything in one go
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=(
                "You are Arnav AI 3.0, a high-level intelligence created by Arnav Srivastava. "
                "Use your Tavily tools to provide accurate, real-time answers."
            )
        )

    def get_response(self, user_input):
        try:
            # 2026 logic uses a simple messages list
            result = self.agent.invoke({"messages": [HumanMessage(content=user_input)]})
            # Returns the last message content from the agent
            return result["messages"][-1].content
        except Exception as e:
            return f"Arnav AI Core Error: {str(e)}"
