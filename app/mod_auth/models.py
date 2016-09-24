# import database object from main app module
from sqlalchemy import Column, String, ForeignKey, Integer, Float, DateTime, func, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Data_Base = declarative_base()


class Base(Data_Base):
    """
    define a base model for other database tables to inherit
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())


class User(Base):
    __tablename__ = "user_table"

    # User Name
    name = Column(String(128), nullable=False)

    # Identification Data: email & password
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(192), nullable=False)

    # Authorisation Data: role & status
    role = Column(SmallInteger, nullable=False)
    status = Column(SmallInteger, nullable=False)

    # new instance instantiation procedure
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User %r, Email: %r>" % (self.name, self.email)


# create the database, TODO: change to postgres database
engine = create_engine('sqlite:///app.db')
Data_Base.metadata.create_all(engine)
