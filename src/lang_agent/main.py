from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from src.lang_agent.third_party.linked import scrape_linked_url

if __name__=="__main__":
    llm = ChatOpenAI(
        base_url="http://192.168.0.111:1234/v1",
        model="meta-llama-3-8b-instruct-abliterated-v3",
        max_tokens=500,
        api_key="dummy")
    summary_template = '''
        Given the {source} information can you summarize it into 5 points with 100 words each for a point
        {content}
    '''
    summary_prompt_template = PromptTemplate(input_variables=["source", "content"], template=summary_template)

    chain = summary_prompt_template | llm | StrOutputParser()

    res = chain.invoke(input={
        "source": "LinkedIn",
        "content": scrape_linked_url("https://gist.githubusercontent.com/Tejasvedagiri/c3c850af20fe6714f09ea9173b28c684/raw/aab98931a95cdfe05bfd2e300f9d995446d3def2/tejas_vedagiri_linked_in")
    })

    print(res)
