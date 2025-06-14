# src/db/models.py
from enum import Enum
from sqlalchemy import (
    Table, Column, Integer, String, Text, Boolean, ForeignKey, Enum as SAEnum,
    create_engine, MetaData
)
from sqlalchemy.orm import (
    declarative_base, relationship, sessionmaker
)

# ─── Enums ───────────────────────────────────────────────────────────
class CardType(Enum):
    STRAIN = "Strain"
    CHAOS  = "Chaos"

class CardUseType(Enum):
    DEFAULT = "Default"
    ONGOING = "Ongoing"

# ─── Base & Engine ───────────────────────────────────────────────────
metadata = MetaData()
Base = declarative_base(metadata=metadata)

# ─── Association Tables ──────────────────────────────────────────────
player_strain = Table(
    "player_strain", metadata,
    Column("player_id", Integer, ForeignKey("player.id"), primary_key=True),
    Column("card_id",   Integer, ForeignKey("card.id"),   primary_key=True),
)

player_chaos = Table(
    "player_chaos", metadata,
    Column("player_id", Integer, ForeignKey("player.id"), primary_key=True),
    Column("card_id",   Integer, ForeignKey("card.id"),   primary_key=True),
)

campaign_player = Table(
    "campaign_player", metadata,
    Column("campaign_id",     Integer, ForeignKey("campaign.id"),      primary_key=True),
    Column("player_id",       Integer, ForeignKey("player.id"),        primary_key=True),
    Column("discord_user_id", Integer, ForeignKey("discord_user.id"),  primary_key=True),
)

# ─── Deck & Card ────────────────────────────────────────────────────
class CardDeck(Base):
    __tablename__ = "carddeck"
    id          = Column(Integer, primary_key=True)
    name        = Column(String(100), index=True, nullable=False)
    description = Column(Text)
    type        = Column(SAEnum(CardType), index=True, nullable=False, default=CardType.STRAIN)

    # 1-to-many → Card.deck
    cards      = relationship("Card", back_populates="deck", cascade="all, delete-orphan")


class Card(Base):
    __tablename__ = "card"
    id        = Column(Integer, primary_key=True)
    deck_id   = Column(Integer, ForeignKey("carddeck.id"), nullable=False)
    deck      = relationship("CardDeck", back_populates="cards")

    type      = Column(SAEnum(CardType),    index=True, nullable=False)
    use_type  = Column(SAEnum(CardUseType), index=True, nullable=False)
    name      = Column(String(100),         index=True, nullable=False)
    effect    = Column(Text)

    # many-to-many → Player
    strain_players = relationship(
        "Player",
        secondary=player_strain,
        back_populates="strain_cards",
    )
    chaos_players  = relationship(
        "Player",
        secondary=player_chaos,
        back_populates="chaos_cards",
    )

# ─── Player ─────────────────────────────────────────────────────────
class Player(Base):
    __tablename__ = "player"
    id           = Column(Integer, primary_key=True)
    name         = Column(String(100), index=True, nullable=False)
    
    # Player stats
    vigour       = Column(Integer, default=0, nullable=False)
    fortitude    = Column(Integer, default=0, nullable=False)
    mind         = Column(Integer, default=0, nullable=False)
    arcane       = Column(Integer, default=0, nullable=False)

    # Health stats
    max_health          = Column(Integer, default=10, nullable=False)
    current_max_health  = Column(Integer, default=10, nullable=False)
    current_health      = Column(Integer, default=10, nullable=False)
    temporary_health    = Column(Integer, default=0, nullable=False)

    # Armour stats
    max_armour              = Column(Integer, default=0, nullable=False)
    max_armour_break        = Column(Integer, default=0, nullable=False)
    current_armour          = Column(Integer, default=0, nullable=False)
    current_armour_break    = Column(Integer, default=0, nullable=False)

    strain_taken = Column(Integer, default=0, nullable=False)

    strain_cards = relationship(
        "Card",
        secondary=player_strain,
        back_populates="strain_players",
    )
    chaos_cards  = relationship(
        "Card",
        secondary=player_chaos,
        back_populates="chaos_players",
    )

# ─── Discord Guild & User ───────────────────────────────────────────
class DiscordGuild(Base):
    __tablename__ = "discord_guild"
    id    = Column(Integer, primary_key=True)
    name  = Column(String(100), index=True, nullable=False)

    users = relationship("DiscordUser", back_populates="guild", cascade="all, delete-orphan")


class DiscordUser(Base):
    __tablename__ = "discord_user"
    id       = Column(Integer, primary_key=True)
    name     = Column(String(100), index=True, nullable=False)
    guild_id = Column(Integer, ForeignKey("discord_guild.id"), nullable=False)

    guild            = relationship("DiscordGuild", back_populates="users")
    campaign_assocs  = relationship(
        "CampaignPlayerLink",
        back_populates="discord_user",
        cascade="all, delete-orphan",
    )

# ─── Campaigns ───────────────────────────────────────────────────────
class Campaign(Base):
    __tablename__ = "campaign"
    id = Column(Integer, primary_key=True)

    player_assocs = relationship(
        "CampaignPlayerLink",
        back_populates="campaign",
        cascade="all, delete-orphan",
    )

class CampaignPlayerLink(Base):
    __tablename__ = "campaign_player"
    campaign_id     = Column(Integer, ForeignKey("campaign.id"),      primary_key=True)
    player_id       = Column(Integer, ForeignKey("player.id"),        primary_key=True)
    discord_user_id = Column(Integer, ForeignKey("discord_user.id"),  primary_key=True)

    campaign      = relationship("Campaign",      back_populates="player_assocs")
    player        = relationship("Player",        back_populates="campaign_assocs")
    discord_user  = relationship("DiscordUser",  back_populates="campaign_assocs")


# ─── Create engine & tables ─────────────────────────────────────────
def init_db(url: str):
    engine = create_engine(url, echo=True, future=True)
    metadata.create_all(engine)
    return sessionmaker(engine, future=True)
