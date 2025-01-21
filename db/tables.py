import datetime

import sqlalchemy

metadata = sqlalchemy.MetaData()

boards = sqlalchemy.Table('boards', metadata,
                          sqlalchemy.Column(
                              'id', sqlalchemy.Integer(), primary_key=True, autoincrement=True, unique=True,
                          ),
                          sqlalchemy.Column(
                              "size", sqlalchemy.Integer(), primary_key=True, nullable=False,
                          ),
                          sqlalchemy.Column(
                              "map", sqlalchemy.JSON(), nullable=False,
                          ))

games = sqlalchemy.Table('games', metadata,
                         sqlalchemy.Column(
                             'id', sqlalchemy.Integer(), primary_key=True, autoincrement=True, unique=True,
                         ),
                         sqlalchemy.Column(
                             "points", sqlalchemy.Integer(), nullable=False,
                         ),
                         sqlalchemy.Column(
                             "is_win", sqlalchemy.Boolean(), default=False,
                         ),
                         sqlalchemy.Column(
                             "datetime", sqlalchemy.DateTime(), default=datetime.datetime.now,
                         ),
                         sqlalchemy.Column(
                             "board_id", sqlalchemy.ForeignKey("boards.id"), default=None,
                         ))