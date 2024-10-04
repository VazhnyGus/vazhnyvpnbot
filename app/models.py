from dataclasses import dataclass


@dataclass
class UserInfo:
    name: str
    user_id: int
    payment_date: int
    keys: list[tuple[int, str]]
