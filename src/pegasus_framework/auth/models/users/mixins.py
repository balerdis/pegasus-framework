# pegasus_framework/auth/models/users/mixins.py
from sqlalchemy.orm import Mapped

class AuditableUserMixin:
    created_by_id: Mapped[int | None]
    updated_by_id: Mapped[int | None]


class OwnableUserMixin:
    owner_id: Mapped[int | None]