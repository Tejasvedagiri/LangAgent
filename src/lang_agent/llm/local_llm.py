from langchain_openai import ChatOpenAI
from lang_agent.decorators.singleton import singleton_with_variable
from langchain_core.language_models import BaseLanguageModel

@singleton_with_variable
class LocalLLM:
    llm = None
    def __init__(self):
        self.llm = ChatOpenAI(
                        temperature=0,
                        base_url="http://192.168.0.111:1234/v1",
                        model="meta-llama-3-8b-instruct-abliterated-v3",
                        max_tokens=500,
                        api_key="dummy"
        )

    def get_llm(self) -> BaseLanguageModel:
        return self.llm