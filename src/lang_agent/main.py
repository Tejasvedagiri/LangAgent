from lang_agent.agent.linkedin_scraper import LinkedInScraper
from lang_agent.agent.url_agent import UrlAgent
from lang_agent.llm.local_llm import LocalLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv


if __name__=="__main__":
    load_dotenv()
    url_agent = UrlAgent(
        name_of_person="Tejas Vedagiri",
        website="LinkedIn"
    )
    res = url_agent.invoke()
    linkedin_scrapper = LinkedInScraper(
        linkedin_profile_url=res["output"]
    )
    res = linkedin_scrapper.invoke()
    print(res["output"])
    summary_template = '''
    #         Given the {source} information can you summarize it into 5 points with 100 words each for a point
    #         {content}
    #     '''
    summary_prompt_template = PromptTemplate(input_variables=["source", "content"], template=summary_template)
    chain = summary_prompt_template | LocalLLM().get_llm() | StrOutputParser()
    res = chain.invoke(input={
        "source": "LinkedIn",
        "content": res["output"]
    })
    print(res)