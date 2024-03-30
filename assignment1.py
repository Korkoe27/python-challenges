import sqlite3
from datetime import datetime
# A class that represents a store with a database connection to an inventory
# database. The class is used to manage product and sales data stored in this database

class Store:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
         # Create the tables for the product and sales data
        self.create_tables()

    def create_tables(self):
#Create the tables for the products and sales data in the database if they aren't 
#already in the database
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Product (
                            product_id INTEGER PRIMARY KEY,
                            product_name TEXT,
                            product_price REAL,
                            product_quantity INTEGER)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Sales (
                            sale_id INTEGER PRIMARY KEY,
                            sale_date TEXT,
                            product_name TEXT,
                            sale_total REAL)''')
        self.conn.commit()

    def addProduct(self, name, price, quantity):
        self.cur.execute("INSERT INTO Product (product_name, product_price, product_quantity) VALUES (?, ?, ?)", (name, price, quantity))
        self.conn.commit()

    def removeProduct(self, product_id):
        self.cur.execute("DELETE FROM Product WHERE product_id=?", (product_id,))
        self.conn.commit()

    def updateProduct(self, product_id, name, price, quantity):
        self.cur.execute("UPDATE Product SET product_name=?, product_price=?, product_quantity=? WHERE product_id=?", (name, price, quantity, product_id))
        self.conn.commit()

    def displayProducts(self):
        self.cur.execute("SELECT * FROM Product")
        rows = self.cur.fetchall()
        print("Product ID | Product Name | Price | Quantity")
        for row in rows:
            print(f"{row[0]} | {row[1]} | R{row[2]} | {row[3]}")

    def sellProduct(self, product_id, sale_date, sale_quantity):

        #Sell a product with the given product name and quantity. If the product
        #has enough quantity, the product's quantity will be changed and the
        #sale total will be recorded in the sales table. If the product does not
        #have sufficient quantity, there won't be any changes
    
        self.cur.execute("SELECT product_quantity FROM Product WHERE product_id=?", (product_id,))
        row = self.cur.fetchone()
        if row is None:
            print("Product not found!")
            return
        available_quantity = row[0]
        if available_quantity < sale_quantity:
            print("Insufficient quantity!")
            return
        new_quantity = available_quantity - sale_quantity
        self.cur.execute("UPDATE Product SET product_quantity=? WHERE product_id=?", (new_quantity, product_id))
        sale_total = self.cur.execute("SELECT product_price FROM Product WHERE product_id=?", (product_id,)).fetchone()[0] * sale_quantity
        self.cur.execute("INSERT INTO Sales (sale_date, product_name, sale_total) VALUES (?, (SELECT product_name FROM Product WHERE product_id=?), ?)", (sale_date, product_id, sale_total))
        self.conn.commit()
        print(f"Sale successful. Total: R{sale_total}")

    def _del_(self):
        self.conn.close()

def main():
    store = Store("inventory.db")

    while True:
        print("\n===== MENU =====")
        print("1. Add Product")
        print("2. Remove Product")
        print("3. Update Product")
        print("4. Display Products")
        print("5. Sell Product")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            quantity = int(input("Enter product quantity: "))
            store.addProduct(name, price, quantity)
        elif choice == '2':
            product_id = int(input("Enter product ID to remove: "))
            store.removeProduct(product_id)
        elif choice == '3':
            product_id = int(input("Enter product ID to update: "))
            name = input("Enter new product name: ")
            price = float(input("Enter new product price: "))
            quantity = int(input("Enter new product quantity: "))
            store.updateProduct(product_id, name, price, quantity)
        elif choice == '4':
            store.displayProducts()
        elif choice == '5':
            product_id = int(input("Enter product ID to sell: "))
            sale_date = datetime.now().strftime('%Y-%m-%d')
            sale_quantity = int(input("Enter sale quantity: "))
            store.sellProduct(product_id, sale_date, sale_quantity)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "_main_":
    main()