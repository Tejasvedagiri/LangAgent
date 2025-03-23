from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

if __name__=="__main__":
    llm = ChatOpenAI(
        base_url="http://192.168.0.111:1234/v1",
        model="deepseek-r1-distill-llama-8b-abliterated",
        max_tokens=250,
        api_key="dummy")
    summary_template = '''
    Given a {object} describe 
    1. How does it look
    2. What can i do with it
    '''
    summary_prompt_template = PromptTemplate(input_variables=["object"], template=summary_template)

    chain = summary_prompt_template | llm | StrOutputParser()

    res = chain.invoke(input={
        "object": "table"
    })

    print(res)
