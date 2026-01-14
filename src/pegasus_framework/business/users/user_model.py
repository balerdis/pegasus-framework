# pegasus_framework/business/users/user_model.py
import email
from sqlalchemy import (
    Column, 
    Integer, 
    String
)

from pegasus_framework.db.models.base import Base

from pegasus_framework.db.models.mixins import AuditMixin

class User(AuditMixin, Base):

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), index=False)
    last_name = Column(String(255), index=False)
    address = Column(String(255), index=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), index=False)

