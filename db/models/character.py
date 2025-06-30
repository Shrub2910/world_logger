from db.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint

class Character(Base):
    __tablename__ = "characters"
    __table_args__ = (
        UniqueConstraint("world_id", "name", name="uq_world_character_name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    image: Mapped[str] = mapped_column()
    thumbnail: Mapped[str] = mapped_column()
    world_id: Mapped[int] = mapped_column(ForeignKey("worlds.id"))
    world: Mapped["World"] = relationship("World", back_populates="characters")

    

