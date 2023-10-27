from sqlalchemy import Integer, LargeBinary, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship, object_session
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy
import datetime
from typing import List
from typing import Optional

from .database import Base

card_has_tags = Table(
    "card_has_tags",
    Base.metadata,
    Column("card", ForeignKey("card.id", ondelete="CASCADE"), primary_key=True),
    Column("tag", ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True),
)

event_has_cards = Table(
    "event_has_cards",
    Base.metadata,
    Column("event", ForeignKey("event.id", ondelete="CASCADE"), primary_key=True),
    Column("card", ForeignKey("card.id", ondelete="CASCADE"), primary_key=True),
)

class Tag(Base):
    __tablename__ = "tag"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    cards: Mapped[List["Card"]] = relationship(secondary=card_has_tags, back_populates="tags", lazy=True)

class Card(Base):
    __tablename__ = "card"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(index=True, unique=True)
    rarity: Mapped[int] = mapped_column(nullable=False)
    image: Mapped[bytes] = mapped_column(LargeBinary, deferred=True, nullable=True)
    tags: Mapped[List[Tag]] = relationship(secondary=card_has_tags, back_populates="cards")
    @property
    def tags_ids(self):
        return list(map(lambda t: t.id, object_session(self).query(Tag).with_parent(self).add_column(column=Tag.id)))
    upgrades: Mapped[List["CardUpgrade"]] = relationship(back_populates="card", foreign_keys="CardUpgrade.card_id", cascade="save-update, merge, delete, delete-orphan")
    upgrade_requirements: Mapped[List["CardUpgrade"]] = relationship(back_populates="requirement", foreign_keys="CardUpgrade.requirement_id")
    events: Mapped[List["Event"]] = relationship(secondary=event_has_cards, back_populates="cards")
    @property
    def events_ids(self):
        return list(map(lambda e: e.id, object_session(self).query(Event).with_parent(self).add_column(column=Event.id)))
    
class Player(Base):
    __tablename__ = "player"
    discord_id: Mapped[str] = mapped_column(primary_key=True, index=True)
    balance: Mapped[int] = mapped_column(default=0)
    last_daily: Mapped[datetime.datetime] = mapped_column(DateTime)
    daily_streak: Mapped[int] = mapped_column(Integer, default=0)
    card_ownership: Mapped[List['CardOwnership']] = relationship(back_populates='player')

class CardOwnership(Base):
    __tablename__ = "player_has_cards"
    player_id: Mapped[str] = mapped_column(ForeignKey('player.discord_id'), primary_key=True, index=True)
    player: Mapped[Player] = relationship(back_populates='card_ownership')
    card_id: Mapped[int] = mapped_column(ForeignKey("card.id"), primary_key=True)
    # card: Mapped[Card] = relationship(backref='ownership')
    amount: Mapped[int] = mapped_column(nullable=False, default=0)
    
class CardUpgrade(Base):
    __tablename__ = "card_upgrade"
    card_id: Mapped[int] = mapped_column(ForeignKey("card.id"), primary_key=True, index=True)
    card: Mapped["Card"] = relationship(back_populates="upgrades", foreign_keys="CardUpgrade.card_id")
    amount: Mapped[int] = mapped_column(default=1)
    requirement_id: Mapped[int] = mapped_column(ForeignKey("card.id"), primary_key=True)
    requirement: Mapped["Card"] = relationship(back_populates="upgrade_requirements", foreign_keys="CardUpgrade.requirement_id")
    @property
    def requirement_name(self):
        return self.requirement.name

class Event(Base):
    __tablename__ = "event"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    start_time: Mapped[Optional[datetime.datetime]] = mapped_column()
    end_time: Mapped[Optional[datetime.datetime]] = mapped_column()
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str] = mapped_column(unique=False, nullable=True)
    default: Mapped[bool] = mapped_column(nullable=False, default=False)
    cards: Mapped[List[Card]] = relationship(secondary=event_has_cards, back_populates='events')
    @property
    def cards_names(self):
        return list(map(lambda t: t.id, object_session(self).query(Card).with_parent(self).add_column(column=Card.name)))


# Player.cards = association_proxy('card_ownership', 'player')