import datetime
import sqlalchemy

Base = sqlalchemy.ext.declarative.declarative_base()


class Game(Base):
    __tablename__ = "games"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    points = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    is_win = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    map = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)
    size = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    steps = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    @classmethod
    def get_best_score(cls, session):
        best_score = session.query(sqlalchemy.func.max(cls.points)).scalar()
        return best_score

    @classmethod
    def get_top_3_games(cls, session):
        top_games = session.query(cls).order_by(sqlalchemy.desc(cls.points)).limit(3).all()
        return top_games
