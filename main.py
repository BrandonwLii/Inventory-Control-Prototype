from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
from pydantic import BaseModel
from db import InventoryItem, ReportItem, engine
from sqlmodel import SQLModel, Session, select, delete

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
def deleteInventoryItem(item_SKU: int, session: SessionDep):
    item = session.get(InventoryItem, item_SKU)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()

    return {"ok": True}

@app.post("/reports/{item_SKU}")
def addReportItem(item_SKU: int, session: SessionDep) -> ReportItem:
    invitem = session.get(InventoryItem,item_SKU)

    if not invitem:
        raise HTTPException(status_code=404, detail="Item not found")

    repItem = session.get(ReportItem, {"Quality" : invitem.Quality, "Width" : invitem.Width, "Thickness" : invitem.Thickness})

    if not repItem:
        session.add(ReportItem(Quality = invitem.Quality, Width = invitem.Width,Thickness = invitem.Thickness,Quantity = 1))
    else:
        repItem.Quantity = repItem.Quantity + 1
        session.add(repItem)
        session.commit

@app.get("/reports/tally")
def generateReport(session: SessionDep) -> list[ReportItem]:
    return session.exec(select(ReportItem)).all()

