from sqlalchemy import create_engine
from sqlalchemy.orm import relationships, sessionmaker, scoped_session
import config
from contextlib import contextmanager

class DataBase():
    def __init__(self,**kwargs):
        if 'db_echo' not in kwargs:
            kwargs['db_echo'] = False
        if 'db_pool_size' not in kwargs:
            kwargs['db_pool_size'] = 10
        self.engine = create_engine(kwargs['db_url'],
                                    echo=kwargs['db_echo'],
                                    pool_size=kwargs['db_pool_size'],
                                    echo_pool=True)
        if 'autoflush' not in kwargs:
            kwargs['autoflush'] = False
        if 'autocommit' not in kwargs:
            kwargs['autocommit'] = False

        self.autocommit = kwargs['autocommit']
        self.autoflush = kwargs['autoflush']
        self.sess = scoped_session(sessionmaker(autocommit=self.autocommit,
                                                autoflush=self.autoflush,
                                                bind=self.engine))

database = DataBase(db_url=config.db_url,db_echo=config.db_echo,db_pool_size=config.db_pool_size)

@contextmanager
def session_scope(commit=True):
    session = database.sess()
    try:
        yield session
        if commit:
            session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()