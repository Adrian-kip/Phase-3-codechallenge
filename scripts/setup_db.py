import sqlite3

def setup():
    conn = sqlite3.connect("articles.db")
    with open("lib/db/schema.sql") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup()
    print("Database schema created!")
