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
                unit TEXT,
                bought BOOLEAN
            )
        ''')
        self.connection.commit()

    def add_item(self, item_name, quantity, unit, bought):
        self.cursor.execute('''
            INSERT INTO shopping_list (item_name, quantity, unit, bought)
            VALUES (?, ?, ?, ?)
        ''', (item_name, quantity, unit, bought))
        self.connection.commit()

    def get_items(self):
        self.cursor.execute('SELECT * FROM shopping_list')
        
        return self.cursor.fetchall()

    def delete_item(self, item_id):
        self.cursor.execute('DELETE FROM shopping_list WHERE id = ?', (item_id,))
        self.connection.commit()
    
    def update_item(self, item_name, quantity, unit, bought):
        unit = unit.strip().lower().replace('.', '')
        item_name = item_name.strip().capitalize()
        self.cursor.execute('''
            SELECT id FROM shopping_list
            WHERE item_name = ? AND unit = ?
        ''', (item_name, unit))

        result = self.cursor.fetchone()
        if result is None:
            self.add_item(item_name, quantity, unit, bought)
            return
        
        item_id = result[0]
        self.cursor.execute('''
            UPDATE shopping_list
            SET quantity = ?, bought = ?
            WHERE id = ?
        ''', (quantity, bought, item_id))
        self.connection.commit()
    
    def update_quantity(self, item, quantity, unit, bought=False):
        unit = unit.strip().lower().replace('.', '')
        item = item.strip().capitalize()
        self.cursor.execute('''
            SELECT id, quantity FROM shopping_list
            WHERE item_name = ? AND unit = ?
        ''', (item, unit))

        result = self.cursor.fetchone()
        if result is None:
            self.add_item(item, quantity, unit, bought)
            return
        
        item_id, current_quantity = result
        quantity += current_quantity
        self.cursor.execute('''
            UPDATE shopping_list
            SET quantity = ?
            WHERE item_name = ? AND unit = ?
            
        ''', (quantity, item, unit))
        self.connection.commit()

    def update_bought_status(self, item_id, bought):
        self.cursor.execute('''
            UPDATE shopping_list
            SET bought = ?
            WHERE id = ?
        ''', (bought, item_id))
        self.connection.commit()

    def close(self):
        self.connection.close()

if __name__ == "__main__":
    with ShoppingListDatabase() as db:
        db.update_item("Jajka", 12, "szt")