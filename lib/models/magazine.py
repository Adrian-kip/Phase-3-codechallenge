from lib.db.connection import get_connection

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    @classmethod
    def create(cls, name, category):
        if not name or not isinstance(name, str):
            raise ValueError("Magazine name must be a non-empty string.")
        if not category or not isinstance(category, str):
            raise ValueError("Magazine category must be a non-empty string.")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (name, category))
        conn.commit()
        return cls(cursor.lastrowid, name, category)

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        return cls(row["id"], row["name"], row["category"]) if row else None

    def contributors(self):
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT a.* FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        return [Author(row["id"], row["name"]) for row in rows]

    def articles(self):
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        return [Article(row["id"], row["title"], row["author_id"], row["magazine_id"]) for row in rows]

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        return [row["title"] for row in rows]
