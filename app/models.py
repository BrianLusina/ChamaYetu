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

    username = first_name.lower() + last_name.lower() + "@" + chama_group

    chama_id = Column(Integer, ForeignKey('chama_groups.id'))
    chama = relationship(ChamaGroup)

    # new instance instantiation procedure
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User %r\n" % self.name + "<Contact:{Email: %r, Number:%r}>\n" % (self.email, self.phone_number)


class ChamaGroup(Base):
    """
    The Chama group table. Will contain a table for all the chamas in the database
    Attributes:
        name: name of the chama
    """

    __tablename__ = "chama_groups"

    name = Column(String(130), nullable=False)
    total_amount = Column(Integer, nullable=True)


# create the database, TODO: change to postgres database
engine = create_engine('sqlite:///app.db')
Data_Base.metadata.create_all(engine)
