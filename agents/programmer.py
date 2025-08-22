from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
from agents.tools import SandboxExecutor

def run_programmer(task_description: str, llm: Ollama, sandbox: SandboxExecutor) -> str:
    """
    Runs the programmer agent to generate and execute Python code.

    Args:
        task_description (str): The description of the task for the programmer.
        llm (Ollama): The Ollama LLM instance.
        sandbox (SandboxExecutor): The sandbox executor for running the code.

    Returns:
        str: The result of the code execution.
    """
    # Define the prompt template for the programmer agent
    programmer_template = """
    You are a Python programmer. Your task is to write a Python script to accomplish the following task.
    Do not add any explanation, just the code.

    Task: {task_description}

    Your code should be a single block of Python code.
    """

    prompt = PromptTemplate(
        template=programmer_template,
        input_variables=["task_description"],
    )

    # Create the chain
    chain = prompt | llm

    # Invoke the chain to get the Python code
    python_code = chain.invoke({"task_description": task_description})

    # Execute the code in the sandbox
    result = sandbox._run(python_code)

    return result
