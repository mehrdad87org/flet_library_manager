import sqlite3
import flet as ft

class LibraryManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        sql_create_table_cmd = '''
CREATE TABLE IF NOT EXISTS library (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    bprice REAL,
    aprice REAL,
    inventario INTEGER
)'''
        self.cursor.execute(sql_create_table_cmd)
        self.conn.commit()

    def add_item(self, name, bprice, aprice, inventario):
        self.cursor.execute("INSERT INTO library (name, bprice, aprice, inventario) VALUES (?, ?, ?, ?)", (name, bprice, aprice, inventario))
        self.conn.commit()

    def search_item(self, item_id):
        self.cursor.execute("SELECT * FROM library WHERE id=?", (item_id,))
        return self.cursor.fetchone()

    def delete_item(self, item_id):
        self.cursor.execute("DELETE FROM library WHERE id=?", (item_id,))
        self.conn.commit()

    def edit_item(self, item_id, bprice, aprice, inventario):
        self.cursor.execute("UPDATE library SET bprice=?, aprice=?, inventario=? WHERE id=?", (bprice, aprice, inventario, item_id))
        self.conn.commit()

    def clear_database(self):
        self.cursor.execute("DELETE FROM library")
        self.conn.commit()

    def close(self):
        self.conn.close()

class LibraryApp:
    def __init__(self, page, manager):
        self.manager = manager
        self.page = page
        self.page.title = "Library Management"
        self.create_widgets()
        self.page.on_close = self.on_close

    def create_widgets(self):
        self.entry_id = ft.TextField(label="ID")
        self.entry_name = ft.TextField(label="Name product")
        self.entry_purchase_price = ft.TextField(label='Purchase price')
        self.entry_selling_price = ft.TextField(label="Selling price")
        self.entry_quantity = ft.TextField(label="Quantity")

        self.add_button = ft.ElevatedButton(text="Add item", on_click=self.add_item, bgcolor=ft.colors.GREEN)
        self.search_button = ft.ElevatedButton(text="Search item", on_click=self.search_item, bgcolor=ft.colors.YELLOW)
        self.delete_button = ft.ElevatedButton(text="Delete item", on_click=self.delete_item, bgcolor=ft.colors.BLUE)
        self.edit_button = ft.ElevatedButton(text="Edit", on_click=self.edit_item, bgcolor=ft.colors.ORANGE)
        self.clear_db_button = ft.ElevatedButton(text="Delete all", on_click=self.clear_database, bgcolor=ft.colors.PURPLE)
        self.quit_button = ft.ElevatedButton(text="Quit", on_click=self.page.close, bgcolor=ft.colors.RED)

        self.page.add(
            ft.Container(
                content=ft.Column([
                    self.entry_id,
                    self.entry_name,
                    self.entry_purchase_price,
                    self.entry_selling_price,
                    self.entry_quantity,
                    ft.Row([self.add_button, self.search_button, self.delete_button]),
                    ft.Row([self.edit_button, self.clear_db_button, self.quit_button])
                ]),
                padding=20,
                border_radius=10,
                border=ft.border.all(color=ft.colors.BLACK)
            )
        )

    def clear_fields(self):
        self.entry_id.value = ""
        self.entry_name.value = ""
        self.entry_purchase_price.value = ""
        self.entry_selling_price.value = ""
        self.entry_quantity.value = ""
        self.page.update()

    def add_item(self, event):
        name = self.entry_name.value
        purchase_price = float(self.entry_purchase_price.value)
        selling_price = float(self.entry_selling_price.value)
        quantity = int(self.entry_quantity.value)
        self.manager.add_item(name, purchase_price, selling_price, quantity)
        self.clear_fields()

    def search_item(self, event):
        item_id = self.entry_id.value
        item = self.manager.search_item(item_id)
        if item:
            print(f"ID: {item[0]}, commodity: {item[1]}, purchase price : {item[2]}, Selling price: {item[3]}, inventario : {item[4]}")
        else:
            print("Product not found!")

    def delete_item(self, event):
        item_id = self.entry_id.value
        self.manager.delete_item(item_id)
        self.clear_fields()

    def edit_item(self, event):
        item_id = self.entry_id.value
        purchase_price = float(self.entry_purchase_price.value)
        selling_price = float(self.entry_selling_price.value)
        quantity = int(self.entry_quantity.value)
        self.manager.edit_item(item_id, purchase_price, selling_price, quantity)
        self.clear_fields()

    def clear_database(self, event):
        self.manager.clear_database()

    def on_close(self, event):
        self.manager.close()

def main(page: ft.Page):
    manager = LibraryManager('library.db')
    app = LibraryApp(page, manager)

ft.app(target=main)
