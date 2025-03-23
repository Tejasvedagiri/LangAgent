from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from src.lang_agent.third_party.linked import scrape_linked_url
from langchain_core.tools import Tool
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from src.lang_agent.tool.tavily_crawler import get_profile_url_tavily
from dotenv import load_dotenv


if __name__=="__main__":
    load_dotenv()
    name= "Tejas Vedagiri"
    llm = ChatOpenAI(
        temperature=0,
        base_url="http://192.168.0.111:1234/v1",
        model="meta-llama-3-8b-instruct-abliterated-v3",
        max_tokens=500,
        api_key="dummy")
    template = '''
        Given the full name of {name_of_person}. I want you to get me the LinkedIn profile page URL.
        The answer must only contain the LinkedIn URL.
    '''
    prompt_template = PromptTemplate(input_variables=["name_of_person"], template=template)

    tools_for_agent = [
        Tool(
            name="Crawl Google for LinkedIn Profile Page",
            func=get_profile_url_tavily,
            description="Method to get LinkedIn Profile Page URL"
        )
    ]
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm,
                               tools=tools_for_agent,
                               prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent,
                                   tools=tools_for_agent,
                                   verbose=True)
    result = agent_executor.invoke(
        input={
            "input": prompt_template.format_prompt(name_of_person=name)
        }
    )
    print(result["output"])
#
#     chain = summary_prompt_template | llm | StrOutputParser()
#
#     res = chain.invoke(input={
#         "source": "LinkedIn",
#         "content": scrape_linked_url("https://gist.githubusercontent.com/Tejasvedagiri/c3c850af20fe6714f09ea9173b28c684/raw/aab98931a95cdfe05bfd2e300f9d995446d3def2/tejas_vedagiri_linked_in")
#     })
#
#     print(res)




from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from src.lang_agent.third_party.linked import scrape_linked_url

# if __name__=="__main__":
#     llm = ChatOpenAI(
#         temperature=0,
#         base_url="http://192.168.0.111:1234/v1",
#         model="meta-llama-3-8b-instruct-abliterated-v3",
#         max_tokens=500,
#         api_key="dummy")
#     summary_template = '''
#         Given the {source} information can you summarize it into 5 points with 100 words each for a point
#         {content}
#     '''
#     summary_prompt_template = PromptTemplate(input_variables=["source", "content"], template=summary_template)
#
#     chain = summary_prompt_template | llm | StrOutputParser()
#
#     res = chain.invoke(input={
#         "source": "LinkedIn",
#         "content": scrape_linked_url("https://gist.githubusercontent.com/Tejasvedagiri/c3c850af20fe6714f09ea9173b28c684/raw/aab98931a95cdfe05bfd2e300f9d995446d3def2/tejas_vedagiri_linked_in")
#     })
#
#     print(res)
