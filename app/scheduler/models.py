from enum import Enum
import uuid

from app import db


class TaskType(Enum):
    SAVE_STOCK_PRICE = "SaveStockPrice"


class Period(Enum):
    DAILY = "Daily"
    ONCE = "Once"


class ScheduledTask(db.Model):
    __tablename__ = "scheduled_task"

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(
        db.String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )
    name = db.Column(db.String(100), nullable=False)
    run_time = db.Column(db.Time, nullable=False)
    active = db.Column(db.Boolean, default=True)
    type = db.Column(db.Enum(TaskType), nullable=False)
    period = db.Column(db.Enum(Period), nullable=False)

    def __repr__(self):
        return self.name
