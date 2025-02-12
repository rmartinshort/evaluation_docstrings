from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms.mlx_pipeline import MLXPipeline
from langchain_community.chat_models.mlx import ChatMLX
from image_agent.models.config import llama_path
from typing import Any


class LlamaCaller:
    MODEL_PATH = llama_path

    def __init__(
        self, system_prompt: Any, temperature: float = 0, max_tokens: int = 1000
    ) -> None:
        self.system_prompt: Any = system_prompt
        self.loaded_model: MLXPipeline = MLXPipeline.from_model_id(
            self.MODEL_PATH,
            pipeline_kwargs={
                "max_tokens": max_tokens,
                "temp": temperature,
                "do_sample": False,
            },
        )
        self.llm: ChatMLX = ChatMLX(llm=self.loaded_model)
        self.temperature: float = temperature
        self.max_tokens: int = max_tokens
        self.chain: Any = self._set_up_chain()

    def _set_up_chain(self) -> Any:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt.system_template),
                ("human", "{query}"),
            ]
        )
        chain = prompt | self.llm | StrOutputParser()
        return chain

    def call(self, query: str) -> Any:
        return self.chain.invoke({"query": query})
