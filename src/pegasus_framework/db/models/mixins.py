# pegasus_framework/db/models/mixins.py
from sqlalchemy import Column, DateTime, Boolean, func

from sqlalchemy.orm import declarative_mixin

@declarative_mixin
class AuditMixin:
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp()
    )

    modified_at = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )

    habilited = Column(
        Boolean,
        nullable=False,
        server_default="1"
    )

    deleted_at = Column(
        DateTime,
        nullable=True
    )