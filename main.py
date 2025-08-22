import streamlit as st
import os
import sqlite3
from langchain_community.llms import Ollama
from tavily import TavilyClient
from agents.manager import decompose_task, orchestrate_agents

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

            # 1. Decompose the task
            st.write("Decomposing the task...")
            user_query = f"Topic: {topic}\nGoal: {goal}"
            tasks = decompose_task(user_query, llm)

            if tasks:
                st.write("Tasks decomposed successfully!")
                st.subheader("Planned Tasks:")
                for task in tasks:
                    st.write(f"- **Agent:** {task['agent']}, **Task:** {task['description']}")

                # 2. Orchestrate the agents
                st.write("Orchestrating agents...")
                task_ids = orchestrate_agents(tasks, db_conn, llm, tavily)
                st.success(f"Tasks have been created and stored with IDs: {task_ids}")

                # 3. Display the final report
                st.write("Fetching the final report...")
                cursor = db_conn.cursor()
                cursor.execute("SELECT result FROM tasks WHERE agent = 'Writer' AND status = 'completed'")
                report = cursor.fetchone()

                if report:
                    st.subheader("Final Report:")
                    st.markdown(report[0])
                else:
                    st.error("Could not retrieve the final report.")

            else:
                st.error("Failed to decompose the task. Please try again.")

            db_conn.close()

        except Exception as e:
            st.error(f"An error occurred during initialization: {e}")
    else:
        st.warning("Please provide both a topic and a goal.")
