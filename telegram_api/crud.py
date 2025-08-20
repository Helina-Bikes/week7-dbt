from sqlalchemy.orm import Session
from typing import List
from database import engine
from datetime import datetime
from sqlalchemy import text

def get_top_products(db, limit: int):
    query = text(f"""
        SELECT message_text AS product, COUNT(*) as mentions
        FROM fct_messages
        GROUP BY message_text
        ORDER BY mentions DESC
        LIMIT {limit}
    """)
    result = db.execute(query).fetchall()
    return result

def get_channel_activity(db: Session, channel_name: str):
    query = f"""
        SELECT message_date, COUNT(*) as messages_count
        FROM fct_messages
        WHERE channel_name = '{channel_name}'
        GROUP BY message_date
        ORDER BY message_date;
    """
    result = db.execute(query).fetchall()
    return result

def search_messages(db: Session, keyword: str):
    query = f"""
        SELECT message_id, message, message_date, channel_name
        FROM fct_messages
        WHERE message LIKE '%{keyword}%'
        ORDER BY message_date DESC;
    """
    result = db.execute(query).fetchall()
    return result
