from sqlmodel import Field, Session, SQLModel, create_engine

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None

sqlite_file_name = "database.db"

sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_heroses():
    hero_1 = Hero(name="Iron Man", secret_name="Tony Stark")
    hero_2 = Hero(name="Kapitan Ameryka", secret_name="Steve Rogers")


    with Session(engine) as session:

        session.add(hero_1)
        session.add(hero_2)
        session.commit()
    

def main():
    create_db_and_tables()
    create_heroses()

if __name__ == "__main__":
    main()