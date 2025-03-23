import os
from http.client import responses

import requests
from lang_agent.llm.local_llm import LocalLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain import hub
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_react_agent, AgentExecutor

def get_linked_in_summary(linkedin_profile_url: str):
    api_url = "https://api.scrapin.io/enrichment/profile"
    params = {
        "apikey": os.environ["SCRAPIN_API_KEY"],
        "linkedInUrl": linkedin_profile_url
    }
    response = requests.get(
        api_url, params
    )
    return response.json()


class LinkedInScraper:
    llm = LocalLLM().get_llm()
    react_prompt = hub.pull("hwchase17/react")
    tools = []
    linkedin_profile_url= ""
    template= '''
            Given the LinkedIn profile URL extract the detail summary for a the given user
            {linkedin_profile_url} 
        '''

    def __init__(self, linkedin_profile_url):
        self.linkedin_profile_url = linkedin_profile_url
        self.load_tools()

    def create_prompt(self):
        prompt_template = PromptTemplate(input_variables=["linkedin_profile_url"], template=self.template)
        return prompt_template

    def load_tools(self):
        self.tools.append(Tool(
                name="Get LinkedIn Profile details",
                func=get_linked_in_summary,
                description="This tool provides a method to get users LinkedIn summary given the LinkedIn profile URL"
            )
        )
    def create_agent(self):
        agent = create_react_agent(llm=self.llm,
                                   tools=self.tools,
                                   prompt=self.react_prompt)
        return agent
    def create_executor(self, agent):
        agent_executor = AgentExecutor(agent=agent,
                                       tools=self.tools,
                                       verbose=True,
                                       handle_parsing_errors=True,
                                       max_iterations=1)
        return agent_executor

    def invoke(self):
        prompt_template = self.create_prompt()
        agent = self.create_agent()
        executor = self.create_executor(agent)
        result = executor.invoke(
            input={
                "input": prompt_template.format_prompt(linkedin_profile_url=self.linkedin_profile_url)
            }
        )
        return result

from dotenv import load_dotenv


if __name__=="__main__":
    load_dotenv()
    res = get_linked_in_summary("https://www.linkedin.com/in/tejas-vedagiri-66ab07174")
    print(res)
    print(res.json())