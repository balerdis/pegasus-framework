# pegasus_framework/db/repositories/protocols/soft_delete_model.py
from typing import Protocol
from datetime import datetime
from sqlalchemy.orm import Mapped
class SoftDeleteModel(Protocol):
    id: Mapped[int]
    habilited: Mapped[bool]
    deleted_at: Mapped[datetime | None]
