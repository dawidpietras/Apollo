import sqlite3

class ShoppingListDatabase:
    def __init__(self, db_name=r'db//shopping_list.db'):
        self.db_name = db_name
    
    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_table()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS shopping_list (
                id INTEGER PRIMARY KEY,
                item_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit TEXT
            )
        ''')
        self.connection.commit()

    def add_item(self, item_name, quantity, unit):
        self.cursor.execute('''
            INSERT INTO shopping_list (item_name, quantity, unit)
            VALUES (?, ?, ?)
        ''', (item_name, quantity, unit))
        self.connection.commit()

    def get_items(self):
        self.cursor.execute('SELECT * FROM shopping_list')
        return self.cursor.fetchall()

    def delete_item(self, item_id):
        self.cursor.execute('DELETE FROM shopping_list WHERE id = ?', (item_id,))
        self.connection.commit()
    
    def update_item(self, item, quantity, unit):
        self.cursor.execute('''
            UPDATE shopping_list
            SET quantity = ?,
                unit = ?
            WHERE item_name = ?
            
        ''', (quantity, unit, item))
        self.connection.commit()

    def close(self):
        self.connection.close()

if __name__ == "__main__":
    with ShoppingListDatabase() as db:
        # db.add_item("jajka", 5, "szt")
        # db.add_item("jajka", 10, "szt")
        # db.delete_item(4)
        items = db.get_items()
        for item in items:
            print(item)
        dic = {item[1]: list(item[2:]) for item in items}
        print(dic)
        inputek = {'jajka': [1, 'szt']}
        for key, value in inputek.items():
            if key in dic:
                dic[key][0] += value[0]
            else:
                dic[key] = value
        print(dic)
        for key, value in dic.items():
            db.update_item(key, value[0], value[1])