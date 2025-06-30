from db.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()
    world_id: Mapped[int] = mapped_column(ForeignKey("worlds.id"))
    world: Mapped["World"] = relationship("World", back_populates="characters")

    

