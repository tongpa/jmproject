import os
from datetime import datetime
from hashlib import sha256


#from sqlalchemy.sql import func; 
from sqlalchemy import Table, ForeignKey, Column,and_ ,sql
from sqlalchemy.types import Unicode,   DateTime, Date, Integer, String, Text,Boolean,BigInteger,SmallInteger,CHAR,TIMESTAMP

from sqlalchemy.util import KeyedTuple;
from sqlalchemy.orm import relation, synonym, Bundle
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.mysql import BIT
from pollandsurvey.model import DeclarativeBase, metadata, DBSession
import transaction
import random; 
__all__ = ['UseExtenalLink','MapVoterExtenalLink']





class UseExtenalLink(DeclarativeBase):
    __tablename__ = 'sur_use_external_link'

    id_use_external_link =  Column(BigInteger, autoincrement=True, primary_key=True);
    id_user = Column(BigInteger, nullable=True);
    user_name = Column(String(255), nullable=True);
    user_type = Column(String(255), nullable=True);
    id_test  = Column(BigInteger, nullable=True);
    id_voter = Column(BigInteger,ForeignKey('sur_voter.id_voter'), nullable=True, index=True);
    voter = relation('Voter', backref='sur_use_external_link_id_voter');
    no_test  = Column(Integer, nullable=True);
    id_question_option = Column(BigInteger, nullable=True);
    active  = Column(BIT, nullable=True, default=1);
    create_date = Column(DateTime, default=datetime.now);
     
    def __init__(self):
        self.active = 1;
        self.create_date =  datetime.now();
        
    def save (self):
        
        DBSession.add(self); 
        DBSession.flush() ;
    
    @classmethod
    def getUserLinkBy(cls,idUser,idTest,idPublic):
        return DBSession.query(cls).filter(cls.id_user == str(idUser),cls.id_test == str(idTest),cls.id_question_option == str(idPublic)  ).first();
        
class MapVoterExtenalLink(DeclarativeBase):
    __tablename__ = 'sur_map_voter_external_link'

    id_map_voter_external_link =  Column(BigInteger, autoincrement=True, primary_key=True);
    
    id_use_external_link = Column(BigInteger,ForeignKey('sur_use_external_link.id_use_external_link'), nullable=True,index=True);
    
    id_voter = Column(BigInteger,ForeignKey('sur_voter.id_voter'), nullable=True, index=True);
    voter = relation('Voter', backref='sur_map_voter_external_link_id_voter');
    
    id_user_ref = Column(BigInteger, nullable=True,index=True);
    
    
    
    create_date = Column(DateTime, default=datetime.now);
    update_date = Column(DateTime );
     
    def __init__(self):
        self.active = 1;
        self.create_date =  datetime.now();
        
    def save (self):
        
        DBSession.add(self); 
        DBSession.flush() ;
    
    @classmethod
    def getUserLinkVoterBy(cls,idLink,idUserRef):
        return DBSession.query(cls).filter(cls.id_use_external_link == str(idLink), cls.id_user_ref == str(idUserRef)   ).first();  
    