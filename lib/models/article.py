from lib.db.connection import get_connection

class Article:
    def __init__(self, id: int, title: str, author_id: int, magazine_id: int):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f"<Article id={self.id}, title='{self.title}', author_id={self.author_id}, magazine_id={self.magazine_id}>"

    @classmethod
    def create(cls, title: str, author, magazine):
        """Create and save a new article to the database"""
        if not title or not isinstance(title, str):
            raise ValueError("Article title must be a non-empty string.")
        if not hasattr(author, 'id') or not hasattr(magazine, 'id'):
            raise ValueError("Author and magazine must be saved to database first.")
            
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
            (title, author.id, magazine.id)
        )
        conn.commit()
        return cls(cursor.lastrowid, title, author.id, magazine.id)

    @classmethod
    def find_by_id(cls, article_id: int):
        """Find an article by its ID"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
        row = cursor.fetchone()
        return cls(row["id"], row["title"], row["author_id"], row["magazine_id"]) if row else None

    @classmethod
    def find_by_title(cls, title: str):
        """Find all articles with matching title"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
        rows = cursor.fetchall()
        return [cls(row["id"], row["title"], row["author_id"], row["magazine_id"]) for row in rows]

    @classmethod
    def find_by_author(cls, author):
        """Find all articles by a specific author"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (author.id,))
        rows = cursor.fetchall()
        return [cls(row["id"], row["title"], row["author_id"], row["magazine_id"]) for row in rows]

    @classmethod
    def find_by_magazine(cls, magazine):
        """Find all articles in a specific magazine"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine.id,))
        rows = cursor.fetchall()
        return [cls(row["id"], row["title"], row["author_id"], row["magazine_id"]) for row in rows]

    def author(self):
        """Get the author of this article"""
        from lib.models.author import Author  # Local import to avoid circular dependency
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (self.author_id,))
        row = cursor.fetchone()
        return Author(row["id"], row["name"]) if row else None

    def magazine(self):
        """Get the magazine this article belongs to"""
        from lib.models.magazine import Magazine  # Local import to avoid circular dependency
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (self.magazine_id,))
        row = cursor.fetchone()
        return Magazine(row["id"], row["name"], row["category"]) if row else None

    def update(self, title: str = None, author_id: int = None, magazine_id: int = None):
        """Update article attributes in the database"""
        updates = []
        params = []
        
        if title is not None:
            if not isinstance(title, str):
                raise ValueError("Title must be a string")
            updates.append("title = ?")
            params.append(title)
            
        if author_id is not None:
            updates.append("author_id = ?")
            params.append(author_id)
            
        if magazine_id is not None:
            updates.append("magazine_id = ?")
            params.append(magazine_id)
            
        if not updates:
            return False
            
        params.append(self.id)
        query = f"UPDATE articles SET {', '.join(updates)} WHERE id = ?"
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        
        if cursor.rowcount > 0:
            if title is not None:
                self.title = title
            if author_id is not None:
                self.author_id = author_id
            if magazine_id is not None:
                self.magazine_id = magazine_id
            return True
        return False

    def delete(self):
        """Delete this article from the database"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM articles WHERE id = ?", (self.id,))
        conn.commit()
        return cursor.rowcount > 0