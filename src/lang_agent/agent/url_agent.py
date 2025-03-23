from lang_agent.llm.local_llm import LocalLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain import hub
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_react_agent, AgentExecutor

def get_profile_url_tavily(name: str):
    tavily = TavilySearchResults()
    res = tavily.run(name)
    return res


class UrlAgent:
    llm = LocalLLM().get_llm()
    react_prompt = hub.pull("hwchase17/react")
    tools = []
    name_of_person= ""
    website= ""
    template= '''
            Given the full name of {name_of_person}. I want you to get me the {website} profile page URL.
            The answer must only contain the {website} URL.
        '''

    def __init__(self, name_of_person, website):
        self.name_of_person = name_of_person
        self.website = website
        self.load_tools()

    def create_prompt(self):
        prompt_template = PromptTemplate(input_variables=["name_of_person", "website"], template=self.template)
        return prompt_template

    def load_tools(self):
        self.tools.append(Tool(
                name="Get LinkedIn Profile URL",
                func=get_profile_url_tavily,
                description="This tool provides a method to get users LinkedIn Profile URL"
            )
        )
        self.tools.append(Tool(
            name="Get Facebook Profile URL",
            func=get_profile_url_tavily,
            description="This tool provides a method to get users Facebook Profile URL"
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
                                       handle_parsing_errors=True)
        return agent_executor

    def invoke(self):
        prompt_template = self.create_prompt()
        agent = self.create_agent()
        executor = self.create_executor(agent)
        result = executor.invoke(
            input={
                "input": prompt_template.format_prompt(name_of_person=self.name_of_person, website=self.website)
            }
        )
        return result

