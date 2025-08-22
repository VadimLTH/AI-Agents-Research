from langchain_core.tools import BaseTool
from tavily import TavilyClient
from ai_code_sandbox import AICodeSandbox

class TavilySearchTool(BaseTool):
    """
    A tool for performing searches using the Tavily API.
    """
    name: str = "TavilySearch"
    description: str = "A tool to search the internet for information. The input should be a search query."
    tavily_client: TavilyClient

    def _run(self, query: str) -> str:
        """
        Performs a search using the Tavily API.
        """
        result = self.tavily_client.search(query)
        return str(result)

    async def _arun(self, query: str) -> str:
        """
        Performs an asynchronous search using the Tavily API.
        """
        result = await self.tavily_client.search(query)
        return str(result)

class SandboxExecutor(BaseTool):
    """
    A tool for executing Python code in a sandboxed environment.
    """
    name: str = "SandboxExecutor"
    description: str = "A tool to execute Python code in a sandboxed environment. The input should be a string of Python code."
    sandbox: AICodeSandbox

    def _run(self, code: str) -> str:
        """
        Executes Python code in a sandboxed environment.
        """
        try:
            result = self.sandbox.run(code)
            return str(result)
        except Exception as e:
            return f"An error occurred: {e}"

    def _arun(self, code: str) -> str:
        """
        Executes Python code in a sandboxed environment.
        """
        try:
            result = self.sandbox.run(code)
            return str(result)
        except Exception as e:
            return f"An error occurred: {e}"
