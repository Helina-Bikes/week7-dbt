from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import get_db

app = FastAPI(title="Telegram Analytical API")

@app.get("/api/reports/top-products",response_model=list[schemas.TopProduct])
def top_products(limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_top_products(db, limit)

@app.get("/api/channels/{channel_name}/activity",response_model=list[schemas.ChannelActivity])
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    return crud.get_channel_activity(db, channel_name)

@app.get("/api/search/messages",response_model=list[schemas.MessageSearch])
def search_messages(query: str, db: Session = Depends(get_db)):
    return crud.search_messages(db, query)
