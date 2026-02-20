from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
from uuid import UUID, uuid4

class Message(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    sender_id: UUID
    receiver_id: UUID
    subject: str
    body: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MessageBus:
    def __init__(self):
        self.queues: Dict[UUID, List[Message]] = {}

    def send_message(self, message: Message):
        if message.receiver_id not in self.queues:
            self.queues[message.receiver_id] = []
        self.queues[message.receiver_id].append(message)
        return {"status": "sent", "message_id": message.id}

    def get_messages(self, agent_id: UUID) -> List[Message]:
        messages = self.queues.get(agent_id, [])
        self.queues[agent_id] = [] # Clear after reading (basic queue behavior)
        return messages

message_bus = MessageBus()
