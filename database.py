import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer,  String
from sqlalchemy.ext.declarative import declarative_base
from config import db_name, db_user, db_host, db_password

engine = create_engine(
    'postgresql://{0}:{1}@{2}/{3}'.format(db_user, db_password, db_host, db_name)
)
metadata = MetaData()
Base = declarative_base()


class Movie(Base):
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    link = Column(String)
    style = Column(String)


Base.metadata.create_all(engine)
file_name = 'film1.csv'
df = pd.read_csv(file_name)
df.to_sql(con=engine, index_label='id', name=Movie.__tablename__, if_exists='replace')

