from db.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class World(Base):
    __tablename__ = "worlds"

    id: Mapped[int] = mapped_column(primary_key=True)

    discord_server_id: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    characters: Mapped[list["Character"]] = relationship("Character", back_populates="world", cascade="all, delete-orphan")