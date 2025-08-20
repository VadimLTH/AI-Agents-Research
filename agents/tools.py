from langchain.tools import BaseTool
from tavily import TavilyClient
import os

class TavilySearchTool(BaseTool):
    """
    A tool for performing web searches using the Tavily API.
    """
    name = "tavily_search"
    description = "Useful for when you need to answer questions about current events or the current state of the world"

    def _run(self, query: str):
        """
        Use the tool.
        """
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        response = client.search(query=query, search_depth="advanced")
        return response['results']

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")
