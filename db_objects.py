from sqlalchemy import *  # Could be more selective
from sqlalchemy.dialects.mysql import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Bookmarks(Base):
    __tablename__ = 'Bookmarks'
    UserID = Column(BIGINT(unsigned=True, zerofill=False), nullable=False, primary_key=True)
    Url = Column(VARCHAR(length=512), nullable=False)
    keywords = Column(VARCHAR(length=512), nullable=False)
    CategoriesID = Column(BIGINT(unsigned=True, zerofill=False), nullable=False)
    Screen_path = Column(VARCHAR(length=512), nullable=False)
    Last_screen_update_date = Column(TIMESTAMP, nullable=False)
    Last_visited = Column(TIMESTAMP, nullable=False)

class Categories(Base):
    __tablename__ = 'Categories'
    UserID = Column(BIGINT(unsigned=True, zerofill=False), nullable=False, primary_key=True)
    CategorieID = Column(BIGINT(unsigned=True, zerofill=False), nullable=False)
    Categorie_name = Column(VARCHAR(length=512), nullable=False)

class Sessions(Base):
    __tablename__ = 'Sessions'
    UserID = Column(BIGINT(unsigned=True, zerofill=False), nullable=False, primary_key=True)
    SessionID = Column(VARCHAR(length=64), nullable=False)
    SessionDate = Column(TIMESTAMP, nullable=False)

class Shared_Bookmarks(Base):
    __tablename__ = 'Shared_Bookmarks'
    UserID = Column(BIGINT(unsigned=True, zerofill=False), nullable=False, primary_key=True)
    BookMarkID = Column(BIGINT(unsigned=True, zerofill=False), nullable=False)
    type = Column(TINYINT(unsigned=True, zerofill=False), nullable=False)
    Shared_to = Column(MEDIUMTEXT, nullable=False)

class Users(Base):
    __tablename__ = 'Users'
    UserID = Column(BIGINT(unsigned=True, zerofill=False), nullable=False, primary_key=True)
    Password = Column(VARCHAR(length=96), nullable=False)

class User_infos(Base):
    __tablename__ = 'User_infos'
    User_Name = Column(VARCHAR(length=128), nullable=False)
    UserID = Column(BIGINT(unsigned=True, zerofill=False), nullable=False, autoincrement=True, primary_key=True)
    First_name = Column(VARCHAR(length=32), nullable=False)
    Last_name = Column(VARCHAR(length=32), nullable=False)
    Address = Column(VARCHAR(length=128), nullable=False)
    Postal_code = Column(VARCHAR(length=16), nullable=False)
    State = Column(VARCHAR(length=128), nullable=False)
    Country = Column(VARCHAR(length=64), nullable=False)
    Plan = Column(TINYINT(unsigned=True, zerofill=False), nullable=False)
    UserState = Column(TINYINT(unsigned=True, zerofill=False), nullable=False)
