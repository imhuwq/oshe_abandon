import os
import json

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from . import Store

Model = declarative_base()
db_name = 'data-test.sqlite'
cur_dir = os.path.dirname(os.path.abspath(__file__))
db_uri = 'sqlite:///' + os.path.join(cur_dir, db_name)


class Data(Model):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    role = Column(String)
    identity = Column(String)
    data = Column(Text)


class SqlalchemyStore(Store):
    def __init__(self):
        engine = create_engine(db_uri)
        session = scoped_session(sessionmaker(bind=engine))
        self.engine = engine
        self.session = session
        self.Model = Model
        self.Table = Data

        self.create_all()

    def create_all(self):
        self.Model.metadata.create_all(self.engine)

    def drop_all(self):
        self.Model.metadata.drop_all(self.engine)

    def store(self, role, identity, data):
        if not isinstance(data, str):
            data = json.dumps(data)
        row = self.Table(role=role, identity=identity, data=data)
        self.session.add(row)
        self.session.commit()
