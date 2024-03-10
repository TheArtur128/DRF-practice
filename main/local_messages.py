from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Message:
    payload: str
    creation_time: datetime = field(default_factory=datetime.now)


def creation_time_of(creation_time: Optional[datetime]) -> datetime:
    if creation_time is None:
        return datetime.now()

    return creation_time


repository = [Message("ping"), Message("pong")]
