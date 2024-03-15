from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(unsafe_hash=True)
class Message:
    payload: str
    creation_time: datetime = field(default_factory=datetime.now)
    id: Optional[int] = None


def creation_time_of(creation_time: Optional[datetime]) -> datetime:
    if creation_time is None:
        return datetime.now()

    return creation_time


class Repository:
    def __init__(self, *messages: Message) -> None:
        self.__max_message_id = self.__get_max_id(messages)
        self.__message_by_id: dict[int, Message] = dict()

        for message in messages:
            self.save(message)

    def get_by_id(self, id: int) -> Optional[Message]:
        return self.__message_by_id.get(id)

    def get_all(self) -> tuple[Message, ...]:
        return tuple(self.__message_by_id.values())

    def save(self, message: Message) -> None:
        if message.id is not None and message.id > self.__max_message_id:
            self.__max_message_id = message.id

        new_message_id = self.__calculate_new_id()

        message.id = new_message_id
        self.__message_by_id[new_message_id] = message

    def remove_by_id(self, id: int) -> None:
        del self.__message_by_id[id]

    def __calculate_new_id(self) -> int:
        self.__max_message_id += 1

        return self.__max_message_id

    @staticmethod
    def __get_max_id(messages: tuple[Message, ...]) -> int:
        ids = tuple(
            message.id
            for message in messages
            if message.id is not None
        )

        return 0 if len(ids) == 0 else max(ids)


repository = Repository(Message("ping"), Message("pong"))
