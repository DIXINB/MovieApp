from sqlalchemy import create_engine
from config import DevelopmentConfig
from sqlalchemy import  Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


from flask import Flask, render_template

engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI, echo=True)
#engine = create_engine('postgresql://postgres:TGN@localhost/moviedb', echo=True)
db_session=scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query=db_session.query_property()

def init_db():
    import app.models
    Base.metadata.create_all(bind=engine)
	
	
	