from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

DATABASE_URL = 'postgresql://user:password@localhost:5433/3-morpion-lecon'

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)

session = Session()