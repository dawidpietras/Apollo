from models.models import ShoppingItem, ToDoTask
from sqlmodel import create_engine, SQLModel, Session 

sqlite_file_name = "database.db"

sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def insert_shopping_list_item(ingredient: ShoppingItem):

    with Session(engine) as session:
        session.add(ingredient)
        session.commit()
    

def main():
    create_db_and_tables()

if __name__ == "__main__":
    main()