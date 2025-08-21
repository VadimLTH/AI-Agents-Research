from langchain_core.tools import BaseTool
from tavily import TavilyClient

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
