import sqlalchemy.orm
import sqlalchemy.ext.declarative
import sqlalchemy_utils

import project.db.config as config
import project.db.tables as tables


DATABASE_URL = config.settings.DATABASE_URL
engine = sqlalchemy.create_engine(DATABASE_URL)

if not sqlalchemy_utils.database_exists(engine.url):
    sqlalchemy_utils.create_database(engine.url)

tables.Base.metadata.create_all(engine)

SessionLocal = sqlalchemy.orm.sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
