from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def run_critic(report: str, llm):
    """
    Runs the critic agent to evaluate a report and suggest improvements.

    Args:
        report (str): The report to be evaluated.
        llm: The language model instance.

    Returns:
        dict: A dictionary containing suggestions for new tasks.
    """
    # Define the prompt template for the critic agent
    critic_template = \"\"\"
    You are a critic agent. Your role is to evaluate a given report, identify its weaknesses,
    and propose concrete, actionable tasks to improve it. These tasks will be sent to other agents.

    The report is as follows:
    {report}

    Please provide your feedback in the form of a JSON object with a single key "tasks".
    This key should contain a list of dictionaries, where each dictionary represents a new task.
    Each task should have the following keys:
    - "agent": The name of the agent to perform the task (e.g., "Researcher", "Writer").
    - "description": A clear and concise description of the task.
    - "tools": A list of tools the agent should use (can be empty).

    Example:
    {{
        "tasks": [
            {{
                "agent": "Researcher",
                "description": "Find more recent data on the European solar panel market, specifically for Q3 and Q4 of 2024.",
                "tools": ["Tavily Search API"]
            }},
            {{
                "agent": "Writer",
                "description": "Rewrite the 'Market Trends' section to include the new data and provide a more in-depth analysis.",
                "tools": []
            }}
        ]
    }}
    \"\"\"

    prompt = PromptTemplate(
        template=critic_template,
        input_variables=["report"],
    )

    # Create the chain with a JSON output parser
    parser = JsonOutputParser()
    chain = prompt | llm | parser

    # Invoke the chain
    response = chain.invoke({{"report": report}})

    return response
