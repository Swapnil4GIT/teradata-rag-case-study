from dataclasses import dataclass, field
from typing import Any, Optional

from endpoint import AIEndpoint
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

_llm_name = "gpt-4o-mini"
_llm_temp = 0.5


@dataclass
class LLMRequest:
    vectorstore: Any
    query: str = ""
    prompt_name: Optional[str] = ""
    out_schema: Optional[dict[str, Any]] = field(default_factory=dict)
    endpoint: AIEndpoint = field(default_factory=AIEndpoint)
    llm_name: str = _llm_name
    llm_temp: float = _llm_temp

    safety_settings = [
        {"category": "violence", "threshold": 2},
        {"category": "self-harm", "threshold": 1},
        {"category": "sexual", "threshold": 2},
        {"category": "harassment", "threshold": 1},
        {"category": "hate", "threshold": 1},
    ]

    @property
    def llm_text(self) -> str:
        msg = "{input}"
        return msg

    def __post_init__(self) -> None:
        self._llm = self._load()

    def _load(self) -> RunnableWithMessageHistory:
        prompt = open(f"prompts/{self.prompt_name}.txt").read()
        documents = self.endpoint.retrieve_documents(
            query=self.query, vectorstore=self.vectorstore
        )
        for doc in documents:
            prompt += "\n" + doc
        print(prompt)

        llm_model = ChatOpenAI(
            model=self.llm_name,
            temperature=self.llm_temp,
        )

        llm_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt),
                MessagesPlaceholder(variable_name="history"),
                ("human", self.llm_text),
            ]
        )

        history_config = [
            ConfigurableFieldSpec(
                id="session_id",
                annotation=str,
                description="The session ID for the chat history.",
            )
        ]

        llm = RunnableWithMessageHistory(
            llm_prompt | llm_model,
            self.endpoint.get_history,
            input_messages_key="input",
            history_messages_key="history",
            history_factory_config=history_config,
        )

        return llm

    def invoke(self, query: str) -> dict[str, Any]:
        config = {"configurable": {"session_id": "session_id"}}
        response = self._llm.invoke({"input": query}, config=config)

        # print(response)
        return response.content
