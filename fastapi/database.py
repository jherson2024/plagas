from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/plaga"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ✅ Esta función es necesaria para las rutas que usan Depends(get_db)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
