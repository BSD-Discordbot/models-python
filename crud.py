from typing import BinaryIO, List
from sqlalchemy.orm import Session

from . import models, schemas

def get_all_cards(db: Session):
    cards = db.query(models.Card).all()
    return cards

def create_card(db: Session, card: schemas.CardBase):
    db_card = models.Card(name=card.name, rarity=card.rarity)
    db.add(db_card)
    update_card(db, card, db_card)
    return db_card

def update_card(db: Session, card: schemas.CardBase, db_card: models.Card):
    db_card.tags.clear()
    for tag in card.tags_ids:
        db_card.tags.append(get_tag(db, tag))
    db_card.upgrades.clear()
    for upgrade in card.upgrades:
        db_upgrade = models.CardUpgrade(amount=upgrade.amount, card_id=db_card.id, card=db_card, requirement=get_card(db, upgrade.requirement_name), requirement_id=upgrade.requirement_name)
        db_card.upgrades.append(db_upgrade)
    for event in card.events_ids:
        db_card.events.append(get_event(db, event))
    db.commit()
    db.refresh(db_card)
    return db_card

def delete_card(db: Session, name: str):
    card = get_card(db, name)
    if(card != None):
        db.delete(card)
        return db.commit()

def get_card(db: Session, name: str):
    card = db.query(models.Card).filter(models.Card.name == name).first()
    return card

def set_card_image(db: Session, name: str, image: bytes):
    card = get_card(db, name)
    setattr(card, 'image', image)
    return db.commit()

def get_all_tags(db: Session):
    return db.query(models.Tag).all()

def get_tag(db: Session, tag: int):
    return db.query(models.Tag).filter(models.Tag.id == tag).first()

def create_tag(db: Session, tag: schemas.TagBase):
    db_tag = models.Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def delete_tag(db: Session, id: int):
    tag = get_tag(db, id)
    if(tag != None):
        db.delete(tag)
        return db.commit()

def get_all_players(db: Session):
    return db.query(models.Player).all()

def get_player(db: Session, player_id: str):
    return db.query(models.Player).filter(models.Player.discord_id == player_id).first()

def get_all_events(db: Session):
    return db.query(models.Event).all()

def get_event(db: Session, id: int):
    return db.query(models.Event).filter(models.Event.id == id).first()

def create_event(db: Session, event: schemas.EventBase):
    db_event = models.Event()
    db.add(db_event)
    db_event = update_event(db, event, db_event)
    return db_event

def update_event(db: Session, event: schemas.EventBase, db_event: models.Event):
    db_event.cards.clear()
    # for card in event.cards_names:
        # db_event.cards.append(get_card(db, card))
    db_event.default = event.default
    db_event.start_time = event.start_time
    db_event.end_time = event.end_time
    db_event.name = event.name
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, id: int):
    event = get_event(db, id)
    if(event != None):
        db.delete(event)
        db.commit()