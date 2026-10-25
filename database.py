import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = BASE_DIR / "spazio.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurant_info (
            topic TEXT PRIMARY KEY,
            details TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            item_id INTEGER PRIMARY KEY,
            item_name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL,
            available INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def load_restaurant_info():
    connection = get_connection()
    cursor = connection.cursor()

    csv_path = DATA_DIR / "restaurant_info.csv"

    with open(csv_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cursor.execute(
                """
                INSERT OR REPLACE INTO restaurant_info (topic, details)
                VALUES (?, ?)
                """,
                (row["topic"], row["details"])
            )

    connection.commit()
    connection.close()


def load_menu():
    connection = get_connection()
    cursor = connection.cursor()

    csv_path = DATA_DIR / "menu.csv"

    with open(csv_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cursor.execute(
                """
                INSERT OR REPLACE INTO menu
                (item_id, item_name, category, price, available)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    int(row["item_id"]),
                    row["item_name"],
                    row["category"],
                    float(row["price"]),
                    int(row["available"].lower() == "true")
                )
            )

    connection.commit()
    connection.close()


def setup_database():
    create_tables()
    load_restaurant_info()
    load_menu()
    print("Database setup completed successfully!")


if __name__ == "__main__":
    setup_database()