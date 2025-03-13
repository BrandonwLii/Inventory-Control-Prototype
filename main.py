from fastapi import FastAPI, Depends
from typing import Annotated
from pydantic import BaseModel
from db import SQLModel, Session, InventoryItem, engine

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/inventory/")
def createInventoryItem(item: InventoryItem, session: SessionDep) -> InventoryItem:   
    session.add(item)
    session.commit()
    session.refresh(item)

    return item

@app.get("/inventory/{item_SKU}")
def getInventoryItem(item_SKU: int, session: SessionDep) -> InventoryItem:
    item = session.get(InventoryItem, item_SKU)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.delete("/inventory/{item_SKU}")
def deleteInventoryItem(item_SKU: int, session: SessionDep) -> InventoryItem:
    item = session.get(InventoryItem, item_SKU)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()

    return {"ok": True}

