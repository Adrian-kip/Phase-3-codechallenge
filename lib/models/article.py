from lib.db.connection import get_connection

class Article:
    def __init__(self, id, title, author_id, magazine_id):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    @classmethod
    def create(cls, title, author, magazine):
        if not title or not isinstance(title, str):
            raise ValueError("Article title must be a non-empty string.")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
            (title, author.id, magazine.id)
        )
        conn.commit()
        return cls(cursor.lastrowid, title, author.id, magazine.id)

    @classmethod
    def find_by_id(cls, article_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
        row = cursor.fetchone()
        return cls(row["id"], row["title"], row["author_id"], row["magazine_id"]) if row else None

    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
        rows = cursor.fetchall()
        return [cls(row["id"], row["title"], row["author_id"], row["magazine_id"]) for row in rows]

    @classmethod
    def find_by_author(cls, author):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (author.id,))
        rows = cursor.fetchall()
        return [cls(row["id"], row["title"], row["author_id"], row["magazine_id"]) for row in rows]

    @classmethod
    def find_by_magazine(cls, magazine):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine.id,))
        rows = cursor.fetchall()
        return [cls(row["id"], row["title"], row["author_id"], row["magazine_id"]) for row in rows]

    def author(self):
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (self.author_id,))
        row = cursor.fetchone()
        return Author(row["id"], row["name"]) if row else None

    def magazine(self):
        from lib.models.magazine import Magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (self.magazine_id,))
        row = cursor.fetchone()
        return Magazine(row["id"], row["name"], row["category"]) if row else None
