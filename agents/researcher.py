from langchain.prompts import PromptTemplate
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from agents.tools import TavilySearchTool

def run_researcher(task: str, llm, tavily_client, context: str):
    """
    Runs the researcher agent for a given task.

    Args:
        task (str): The research task.
        llm (Ollama): The Ollama LLM instance.
        tavily_client (TavilyClient): The Tavily client instance.
        context (str): The memory context from previous steps.

    Returns:
        str: The research report.
    """
    # Initialize the Tavily search tool
    tools = [TavilySearchTool(tavily_client=tavily_client)]

    # Get the ReAct prompt
    prompt = hub.pull("hwchase17/react")

    # Create the agent
    agent = create_react_agent(llm, tools, prompt)

    # Create the agent executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Define the prompt template for the researcher agent
    researcher_template = \"\"\"
    You are a researcher agent. Your goal is to gather information from the internet and synthesize it into a structured report.
    Review the following recent memory entries to understand the context of the task:
    {context}

    Based on the following research task, use the TavilySearch tool to gather information. Then, synthesize the information into a report with the following structure:

    1.  **Summary**: A brief summary of the findings.
    2.  **Raw Data**: The raw data collected from the search, including snippets and content.
    3.  **Source URLs**: A list of the URLs of the sources used.

    Research Task: {task}

    Begin!
    \"\"\"

    # Create the prompt
    prompt_with_task = PromptTemplate(
        template=researcher_template,
        input_variables=["task", "context"],
    ).format(task=task, context=context)


    # Invoke the agent
    response = agent_executor.invoke({"input": prompt_with_task})

    return response["output"]
