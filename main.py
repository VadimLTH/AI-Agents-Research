import streamlit as st
import os
import sqlite3
from langchain_community.llms import Ollama
from tavily import TavilyClient

# --- Initialization ---

# Initialize Ollama
def get_ollama_llm(model="llama3", host="http://ollama:11434"):
    """Initializes and returns the Ollama LLM instance."""
    return Ollama(model=model, base_url=host)

# Initialize Tavily client
def get_tavily_client():
    """Initializes and returns the Tavily client."""
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        st.error("Tavily API key not found. Please set the TAVILY_API_KEY environment variable.")
        st.stop()
    return TavilyClient(api_key=tavily_api_key)

# Initialize SQLite database
def init_db():
    """Initializes the SQLite database and creates tables if they don't exist."""
    conn = sqlite3.connect('research_agent.db')
    cursor = conn.cursor()

    # Create a table for tasks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            description TEXT,
            status TEXT,
            result TEXT,
            agent TEXT
        )
    ''')
    conn.commit()
    return conn

# --- Streamlit UI ---

st.title("Autonomous AI Research Agent")

# Get user input
topic = st.text_input("Enter the research topic:")
goal = st.text_area("Enter the research goal:")

if st.button("Start Research"):
    if topic and goal:
        st.info("Starting the research process...")

        # Initialize everything
        try:
            llm = get_ollama_llm()
            tavily = get_tavily_client()
            db_conn = init_db()

            st.success("Core components initialized successfully!")

            # Create and run the researcher agent
            from agents.researcher import create_researcher_agent
            researcher_agent = create_researcher_agent(llm)
            result = researcher_agent(topic, goal)

            st.write("**Research Report:**")
            st.write(result['output'])

            db_conn.close()

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please provide both a topic and a goal.")
