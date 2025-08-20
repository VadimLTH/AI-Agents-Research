from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from agents.tools import TavilySearchTool

def create_researcher_agent(llm):
    """
    Creates a researcher agent using a given LLM and tools.
    """
    tools = [TavilySearchTool()]

    prompt_template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought:{agent_scratchpad}
    """

    prompt = PromptTemplate(
        input_variables=["input", "agent_scratchpad", "tool_names", "tools"],
        template=prompt_template
    )

    agent = create_react_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    def run_agent(topic, goal):
        query = f"Topic: {topic}\nGoal: {goal}"
        return executor.invoke({"input": query})

    return run_agent
