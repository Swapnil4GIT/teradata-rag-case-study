from dataclasses import dataclass, field
from typing import Any

from langchain_community.chat_message_histories import ChatMessageHistory


@dataclass
class AIEndpoint:
    context: dict[str, ChatMessageHistory] = field(default_factory=dict)

    def get_history(self, session_id: str) -> ChatMessageHistory:
        """
        Retrieve the chat message history for a given session ID.
        """
        if session_id not in self.context:
            self.context[session_id] = ChatMessageHistory()
        return self.context[session_id]

    def retrieve_documents(self, query: str, vectorstore: Any) -> list[Any]:
        """
        Retrieve documents from the vectorstore based on the query.
        """
        documents = vectorstore.similarity_search(query, k=25)
        documents = [doc.page_content for doc in documents]
        return documents
