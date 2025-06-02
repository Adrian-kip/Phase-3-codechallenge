from lib.db.connection import get_connection

class Magazine:
    def __init__(self, id: int, name: str, category: str):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f"<Magazine id={self.id}, name='{self.name}', category='{self.category}'>"

    @classmethod
    def create(cls, name: str, category: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO magazines (name, category) VALUES (?, ?)", 
            (name, category)
        )
        conn.commit()
        return cls(cursor.lastrowid, name, category)

    @classmethod
    def find_by_id(cls, magazine_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (magazine_id,))
        row = cursor.fetchone()
        return cls(row["id"], row["name"], row["category"]) if row else None

    @classmethod
    def find_by_name(cls, name: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()
        return cls(row["id"], row["name"], row["category"]) if row else None

    @classmethod
    def find_by_category(cls, category: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
        return [cls(row["id"], row["name"], row["category"]) for row in cursor.fetchall()]

    def contributors(self):
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT a.id, a.name 
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
        """, (self.id,))
        return [Author(row["id"], row["name"]) for row in cursor.fetchall()]

    def articles(self):
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        return [Article(row["id"], row["title"], row["author_id"], row["magazine_id"]) for row in cursor.fetchall()]

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        return [row["title"] for row in cursor.fetchall()]

    def contributing_authors(self):
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id, a.name, COUNT(ar.id) as article_count
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
            GROUP BY a.id
            HAVING article_count > 1
        """, (self.id,))
        return [Author(row["id"], row["name"]) for row in cursor.fetchall()]

    @classmethod
    def with_multiple_authors(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.id, m.name, m.category
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
            HAVING COUNT(DISTINCT a.author_id) > 1
        """)
        return [cls(row["id"], row["name"], row["category"]) for row in cursor.fetchall()]

    @classmethod
    def article_counts(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.name, COUNT(a.id) as article_count
            FROM magazines m
            LEFT JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
        """)
        return {row["name"]: row["article_count"] for row in cursor.fetchall()}