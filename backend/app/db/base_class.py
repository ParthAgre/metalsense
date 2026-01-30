from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    All database models will inherit from this class.
    We use SQLAlchemy 2.0 style DeclarativeBase.
    """
    pass