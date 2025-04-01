from sqlmodel import Field, SQLModel, create_engine, Session

class ReportItem(SQLModel, table = True):
    Quality: str = Field(primary_key=True)
    Width: int = Field(primary_key=True)
    Thickness: int = Field(primary_key=True)
    Quantity: int 

class InventoryItem(SQLModel ,table = True):
    SKU: int = Field(primary_key = True, index = True)
    Quality: str
    Thickness: int
    Width: int
    
postgres_url = "postgresql://postgres:admin@localhost:5432/Inventory"

engine = create_engine(postgres_url, echo=True)