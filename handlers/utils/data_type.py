from typing import TypedDict


class CacheUser(TypedDict):
    db_id: int
    lang: str
    role: str
    expire_at: float


class FailsInfo(TypedDict):
    fails: int
    locked_until: float
