from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class PlayerBase(BaseModel):
    discord_id: str

class PlayerList(PlayerBase):
    balance: int
    last_daily: datetime
    daily_streak: int

class Player(PlayerList):
    cards: List['Card'] = []

    class Config:
        from_attributes = True

class TagBase(BaseModel):
    name: str

    class Config:
        from_attributes = True

class TagList(TagBase):
    id: int
    name: str

class Tag(TagList):
    cards: List['Card'] = []

    class Config:
        from_attributes = True

class CardUpgradeBase(BaseModel):
    amount: int
    requirement_name: str

class CardUpgrade(CardUpgradeBase):
    pass

class CardBase(BaseModel):
    name: str
    rarity: int
    tags_ids: List[int] = []
    events_ids: List[int] = []
    upgrades: List["CardUpgrade"] = []
    class Config:
        from_attributes = True

class Card(CardBase):
    id: int


class EventBase(BaseModel):
    name: str
    default: Optional[bool] = False
    start_time: Optional[datetime] = datetime.min
    end_time: Optional[datetime] = datetime.max
    
    class Config:
        from_attributes = True

class Event(EventBase):
    # cards_names: Optional[List[str]] = []
    id: int