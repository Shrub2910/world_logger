from db.models.base import Base
from db.session import engine

if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)