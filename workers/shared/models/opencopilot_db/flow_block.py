import datetime
import uuid

from opencopilot_db.database_setup import Base, engine
from sqlalchemy import Column, String, DateTime, Integer


class Chatbot(Base):
    __tablename__ = 'flow_blocks'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255))
    chatbot_id = Column(String(36), nullable=True)
    flow_id = Column(String(36), nullable=True)
    status = Column(String(255), default='draft')
    type = Column(String(255), default='block')
    next_on_success = Column(String(255), default=None)
    next_on_fail = Column(String(255), default=None)
    order = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)


Base.metadata.create_all(engine)
