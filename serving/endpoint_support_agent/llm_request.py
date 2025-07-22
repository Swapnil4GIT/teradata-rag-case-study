import json
from dataclasses import dataclass, field
from typing import Any, Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

_llm_name = "gpt-4o-mini"
_llm_temp = 0.5


@dataclass
class LLMRequest:
    prompt_name: Optional[str] = ""
    out_schema: Optional[dict[str, Any]] = field(default_factory=dict)

    llm_name: str = _llm_name
    llm_temp: float = _llm_temp

    safety_settings = field(
        default_factory=lambda: {
            "harassment": "block",
            "hate": "block",
            "self_harm": "block",
            "sexual": "block",
            "violence": "block",
        }
    )

    @property
    def llm_text(self) -> str:
        msg = "{input}"

        if self.out_schema != {}:
            schema_txt = (
                json.dumps(self.out_schema, indent=2)
                .replace("{", "{{")
                .replace("}", "}}")
            )

            msg += f"Reminder: Format your response as JSON in the form \n{schema_txt}"
        return msg

    def __post_init__(self) -> None:
        self._llm = self._load()

    def _load(self) -> RunnableWithMessageHistory:
        prompt = open(f"prompts/{self.prompt_name}.txt").read()

        llm_model = ChatOpenAI(
            model=self.llm_name,
            temperature=self.llm_temp,
            safety_settings=self.safety_settings,
            generation_config={"response_mime_type": "application/json"},
        )

        llm_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt),
                ("human", self.llm_text),
            ]
        )

        llm = RunnableWithMessageHistory(
            llm_prompt | llm_model,
            input_messages_key="input",
        )

        return llm

    def invoke(self, query: str) -> dict[str, Any]:
        response = self._llm.invoke({"input": query})

        blocked = response.response_metadata["is_blocked"]
        if blocked:
            raise ValueError("The response was blocked by safety settings.")

        try:
            response_data = json.loads(response.content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {e}")
        return response_data
