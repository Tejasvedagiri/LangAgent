from langchain_community.tools.tavily_search import TavilySearchResults

def get_profile_url_tavily(name: str):
    tavily = TavilySearchResults()
    res = tavily.run(name)
    return res
