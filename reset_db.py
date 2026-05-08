from app.db.base import Base
from app.db.session import engine

print("Creating fresh schema...")

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("Done!")