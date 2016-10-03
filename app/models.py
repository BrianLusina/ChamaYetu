# import database object from main app module
from sqlalchemy import Column, String, ForeignKey, Integer,DateTime, Float, DateTime, func, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from  datetime import datetime

Data_Base = declarative_base()


class Base(Data_Base):
    """
    define a base model for other database tables to inherit
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, nullable=False,server_default=func.now())



class ChamaGroup(Base):
    """
    The Chama group table. Will contain a table for all the chamas in the database
    Attributes:
        name: name of the chama
    """

    __tablename__ = "chama_group"

    name = Column(String(130), nullable=False)
    total_amount = Column(Integer, nullable=True)

class Statement(Base):
    __tablename__ = 'statement'

    amount = Column(Integer, nullable=True)

    #todo: get  time created  as the default of date column
    # date = Column(DateTime, default=func.current_timestamp())
    chama_id = Column(Integer,ForeignKey('chama_group.id'))

    chama = relationship(ChamaGroup)


class User(Base):
    """
    Attribues:
        name: name of the user
        email: user email
        username: user's email which will be a slug,i.e. their name and the name of the chama they are in.
            e.g Peter Doe is part of FinSave Chama, his name will be peterdoe@finsave
        chama_group: The group the user is involved in
        phone_number: user phone number
        role:Authorisation Data: role & status, whether admin(chairperson) member
        status: whether online or offline
        total_contributed: total amt of money contributed to date :type int
    """
    __tablename__ = "user_table"

    first_name = Column(String(128), nullable=False)

    last_name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(192), nullable=False)
    chama_group = Column(String(200), nullable=False)
    phone_number = Column(Integer, nullable=False)
    role = Column(SmallInteger, nullable=False)
    status = Column(SmallInteger, nullable=True)
    total_contributed = Column(Integer)

    user_id = Column(Integer, ForeignKey('user_table.id'))
    provider_id = Column(String(255))
    provider_user_id = Column(String(255))
    access_token = Column(String(255))

    secret = Column(String(255))
    display_name = Column(String(255))
    profile_url = Column(String(512))
    image_url = Column(String(512))
    # username = first_name.lower() + last_name.lower() + "@" + chama_group

    chama_id = Column(Integer, ForeignKey('chama_group.id'))
    chama = relationship(ChamaGroup)




    # new instance instantiation procedure
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User %r\n" % self.name + "<Contact:{Email: %r, Number:%r}>\n" % (self.email, self.phone_number)


# create the database, TODO: change to postgres database
engine = create_engine('sqlite:///app.db')
Data_Base.metadata.create_all(engine)
