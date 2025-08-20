from pydantic import BaseModel
from datetime import datetime

class Message(BaseModel):
    message_id: int
    message_text: str
    message_date: datetime
    channel_name: str
    channel_url: str
    has_media: bool
    media_type: str | None
    media_file_name: str | None

    class Config:
        orm_mode = True


class TopProduct(BaseModel):
    product: str
    mentions: int


class ChannelActivity(BaseModel):
    date: str      # or datetime if you prefer
    message_count: int

class MessageSearch(BaseModel):
    message_id: int
    message_text: str
    channel_name: str
    message_date: str  # or datetime
