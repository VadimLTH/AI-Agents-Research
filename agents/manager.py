import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from agents.researcher import run_researcher

def decompose_task(user_query, llm):
    """
    Decomposes a user's query into a structured list of tasks using an LLM.

    Args:
        user_query (str): The user's research query.
        llm (Ollama): The Ollama LLM instance.

    Returns:
        list: A list of dictionaries, where each dictionary represents a task.
    """
    # Define the prompt template for the manager agent
    manager_template = """
    You are a manager agent responsible for breaking down a user's research request into a series of tasks for a team of agents.
    Based on the user's query, create a list of tasks to be executed by the following agents:
    - Researcher: This agent gathers information from the internet using the Tavily Search API.
    - Writer: This agent writes a cohesive report based on the gathered information.
    - Critic: This agent reviews the report and provides feedback.
    - Programmer: This agent can write and execute Python code for specific tasks.

    The user's query is: {user_query}

    Return a JSON object with a single key "tasks", which is a list of dictionaries.
    Each dictionary should have the following keys:
    - "agent": The name of the agent assigned to the task (e.g., "Researcher", "Writer").
    - "description": A clear and concise description of the task.
    - "tools": A list of tools the agent should use (e.g., ["Tavily Search API"]). For the Writer and Critic agent, this can be an empty list.

    Example:
    {{
        "tasks": [
            {{
                "agent": "Researcher",
                "description": "Gather information about the European solar panel market in 2024.",
                "tools": ["Tavily Search API"]
            }},
            {{
                "agent": "Writer",
                "description": "Write a SWOT analysis of the European solar panel market based on the research.",
                "tools": []
            }}
        ]
    }}
    """

    prompt = PromptTemplate(
        template=manager_template,
        input_variables=["user_query"],
    )

    # Create the chain
    chain = prompt | llm | JsonOutputParser()

    # Invoke the chain
    response = chain.invoke({"user_query": user_query})

    return response.get("tasks", [])

def orchestrate_agents(tasks, db_conn, llm, tavily_client):
    """
    Orchestrates the execution of tasks by inserting them into the database.

    Args:
        tasks (list): A list of task dictionaries from decompose_task.
        db_conn (sqlite3.Connection): The database connection.
        llm (Ollama): The Ollama LLM instance.
        tavily_client (TavilyClient): The Tavily client instance.

    Returns:
        list: A list of task IDs that were inserted into the database.
    """
    cursor = db_conn.cursor()
    task_ids = []

    for task in tasks:
        # Insert the task into the database first
        cursor.execute(
            "INSERT INTO tasks (description, agent, status, result) VALUES (?, ?, ?, ?)",
            (task['description'], task['agent'], 'pending', '')
        )
        db_conn.commit()
        task_id = cursor.lastrowid
        task_ids.append(task_id)

        # If the agent is the Researcher, run the researcher agent
        if task['agent'] == 'Researcher':
            result = run_researcher(task['description'], llm, tavily_client)

            # Update the task with the result
            cursor.execute(
                "UPDATE tasks SET status = ?, result = ? WHERE id = ?",
                ('completed', result, task_id)
            )
            db_conn.commit()

    return task_ids
