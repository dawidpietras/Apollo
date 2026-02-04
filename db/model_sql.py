from models.models import ShoppingItem, ToDoTask
from sqlmodel import create_engine, select, SQLModel, Session
from typing import List

sqlite_file_name = "db/database.db"

sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def insert_shopping_list_item(ingredient: ShoppingItem):

    with Session(engine) as session:
        session.add(ingredient)
        session.commit()

def get_all_items() -> List[ShoppingItem] | None:
    with Session(engine) as session:
        results = session.exec(select(ShoppingItem).order_by(ShoppingItem.bought))
        results = results.all()
    if results:
        return results
    return None

def update_shopping_item_bought_status(item_id: int, bought: bool):
    with Session(engine) as session:
        item = session.get(ShoppingItem, item_id)
        if item:
            item.bought = bought
            session.add(item)
            session.commit()
            session.refresh(item)
