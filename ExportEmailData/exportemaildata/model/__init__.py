# -*- coding: utf-8 -*-
"""The application's model objects"""

from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import scoped_session, sessionmaker, Session
#from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

# Global session manager: DBSession() returns the Thread-local
# session object appropriate for the current web request.
maker = sessionmaker(autoflush=True, autocommit=False,
                     extension=ZopeTransactionExtension())
 
DBSession = scoped_session(maker)


maker2 = sessionmaker(autoflush=True, autocommit=False,
                     extension=ZopeTransactionExtension())
DBSession2 = scoped_session(maker2)

# Base class for all of our model classes: By default, the data model is
# defined with SQLAlchemy's declarative extension, but if you need more
# control, you can switch to the traditional method.
DeclarativeBase = declarative_base()
DeclarativeBase2 = declarative_base()
# There are two convenient ways for you to spare some typing.
# You can have a query property on all your model classes by doing this:
# DeclarativeBase.query = DBSession.query_property()
# Or you can use a session-aware mapper as it was used in TurboGears 1:
# DeclarativeBase = declarative_base(mapper=DBSession.mapper)

# Global metadata.
# The default metadata is the one from the declarative base.
metadata = DeclarativeBase.metadata
metadata2 = DeclarativeBase2.metadata
# If you have multiple databases with overlapping table names, you'll need a
# metadata for each database. Feel free to rename 'metadata2'.
#metadata2 = MetaData()

#####
# Generally you will not want to define your table's mappers, and data objects
# here in __init__ but will want to create modules them in the model directory
# and import them at the bottom of this file.
#
######
 
def init_model(engine1, engine2):
    """Call me before using any of the tables or classes in the model."""

#    DBSession.configure(bind=engine)
    DBSession.configure(bind=engine1)
    DBSession2.configure(bind=engine2)

    metadata.bind = engine1
    metadata2.bind = engine2
    
    
    #from sqlalchemy import Table
    #t_events = Table('job_n_day', metadata2,   autoload=True, autoload_with=metadata2.bind)
    
    #global job_n_day;
    #job_n_day = Table('job_n_day', metadata2,   autoload=True, autoload_with=metadata2.bind ) 


def init_model_one(engine):
    """Call me before using any of the tables or classes in the model."""
    DBSession.configure(bind=engine)

    # If you are using reflection to introspect your database and create
    # table objects for you, your tables must be defined and mapped inside
    # the init_model function, so that the engine is available if you
    # use the model outside tg2, you need to make sure this is called before
    # you use the model.

    #
    # See the following example:

    #global t_reflected

    #t_reflected = Table("Reflected", metadata,
    #    autoload=True, autoload_with=engine)

    #mapper(Reflected, t_reflected)

# Import your model modules here.
import transaction ;

from exportemaildata.model.auth import User, Group, Permission
from exportemaildata.model.email import EmailData,ExportEmail,EmailTemp, StatusExport,TypeEmail;
from exportemaildata.model.email import MapGender,MapPrefix,MapProvince,MapCity,MapCounty;
from exportemaildata.model.jm.jmmodel import MUser ,MUserLang,MUserMapRole,MUserEmail,MUserGeneralSetting,MUserPhone,MUserAddres,MJobAApplicant,MJobAApPiPersonalDatum,MJobAApplicantCertificate,MSysMUserMapAddres,MSysMUserMapPhone
