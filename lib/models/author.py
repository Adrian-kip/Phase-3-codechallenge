from lib.db.connection import get_connection

class Author:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Author id={self.id}, name='{self.name}'>"

    @classmethod
    def create(cls, name: str):
        if not name or not isinstance(name, str):
            raise ValueError("Author name must be a non-empty string.")
            
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
        conn.commit()
        return cls(cursor.lastrowid, name)

    @classmethod
    def find_by_id(cls, author_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (author_id,))
        row = cursor.fetchone()
        return cls(row["id"], row["name"]) if row else None

    @classmethod
    def find_by_name(cls, name: str):
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
        return [Article(row["id"], row["title"], row["author_id"], row["magazine_id"]) for row in cursor.fetchall()]

    def magazines(self):
        from lib.models.magazine import Magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.id, m.name, m.category 
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        return [Magazine(row["id"], row["name"], row["category"]) for row in cursor.fetchall()]

    def add_article(self, magazine, title: str):
        from lib.models.article import Article
        if not title or not isinstance(title, str):
            raise ValueError("Article title must be a non-empty string.")
        if not magazine or not hasattr(magazine, 'id'):
            raise ValueError("Valid magazine instance must be provided.")
            
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
            SELECT DISTINCT m.category 
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        return [row["category"] for row in cursor.fetchall()]

    @classmethod
    def top_author(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id, a.name, COUNT(ar.id) as article_count
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            GROUP BY a.id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        return cls(row["id"], row["name"]) if row else None