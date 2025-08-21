from langchain_core.prompts import PromptTemplate

def run_writer(task: str, llm, research_result: str) -> str:
    """
    Runs the writer agent for a given task.

    Args:
        task (str): The writing task.
        llm (Ollama): The Ollama LLM instance.
        research_result (str): The research result from the researcher agent.

    Returns:
        str: The generated report.
    """
    # Define the prompt template for the writer agent
    writer_template = \"\"\"
    You are a writer agent. Your goal is to write a cohesive and well-structured report based on the provided research data.
    The user's request is: {task}
    The research data is: {research_result}

    Based on the above, please generate a Markdown report that is well-structured, with a title, introduction, main body with sections, and a conclusion.
    The report should be easy to read and understand.
    \"\"\"

    prompt = PromptTemplate(
        template=writer_template,
        input_variables=["task", "research_result"],
    )

    # Create the chain
    chain = prompt | llm

    # Invoke the chain
    response = chain.invoke({"task": task, "research_result": research_result})

    return response
