from lib.db.connection import get_connection

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def create(cls, name):
        if not name or not isinstance(name, str):
            raise ValueError("Author name must be a non-empty string.")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
        conn.commit()
        return cls(cursor.lastrowid, name)

    @classmethod
    def find_by_id(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (author_id,))
        row = cursor.fetchone()
        return cls(row["id"], row["name"]) if row else None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = cursor.fetchone()
        return cls(row["id"], row["name"]) if row else None

    def articles(self):
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        rows = cursor.fetchall()
        return [Article(row["id"], row["title"], row["author_id"], row["magazine_id"]) for row in rows]

    def magazines(self):
        from lib.models.magazine import Magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        return [Magazine(row["id"], row["name"], row["category"]) for row in rows]

    def add_article(self, magazine, title):
        from lib.models.article import Article
        if not title or not isinstance(title, str):
            raise ValueError("Article title must be a non-empty string.")
        if not magazine:
            raise ValueError("Magazine must be provided.")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
            (title, self.id, magazine.id)
        )
        conn.commit()
        return Article(cursor.lastrowid, title, self.id, magazine.id)

    def topic_areas(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        return [row["category"] for row in rows]
