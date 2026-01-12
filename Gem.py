import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch  # Updated 2026 package
from langchain.agents import create_agent   # The modern 2026 replacement
from langchain_core.messages import HumanMessage

class ArnavAI:
    def __init__(self):
        # 1. Access keys from Streamlit Secrets
        google_key = st.secrets["GOOGLE_API_KEY"]
        tavily_key = st.secrets["TAVILY_API_KEY"]
        
        # 2. Setup the Free Brain (Gemini 1.5 Flash)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", 
            google_api_key=google_key,
            temperature=0.3
        )
        
        # 3. Setup the Internet Tool
        os.environ["TAVILY_API_KEY"] = tavily_key
        self.search_tool = TavilySearch(max_results=3)
        self.tools = [self.search_tool]

        # 4. Create the Agent (The modern 2026 way)
        # create_agent handles memory and orchestration automatically
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=(
                "You are Arnav AI 3.0, a high-level intelligence created by Arnav Srivastava. "
                "Use your internet tools to provide brilliant, real-time answers."
            )
        )

    def get_response(self, user_input):
        try:
            # Simple invocation for 2026 agents
            result = self.agent.invoke({"messages": [HumanMessage(content=user_input)]})
            # Extract the final message content from the response
            return result["messages"][-1].content
        except Exception as e:
            return f"Arnav AI 3.0 encountered a core issue: {str(e)}"
