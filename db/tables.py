from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, DateTime, VARCHAR, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc

Base = declarative_base()

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    points = Column(Integer, nullable=False)
    is_win = Column(Boolean, default=False)
    datetime = Column(DateTime, default=datetime.now)
    map = Column(VARCHAR, nullable=False)
    size = Column(Integer, nullable=False)
    steps = Column(Integer, nullable=False)

    @classmethod
    def get_best_score(cls, session):
        best_score = session.query(func.max(cls.points)).scalar()
        return best_score

    @classmethod
    def get_top_3_games(cls, session):
        top_games = session.query(cls).order_by(desc(cls.points)).limit(3).all()
        return top_games
