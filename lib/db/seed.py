from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

def reset_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()

def seed_data():
    reset_database()

    author1 = Author.create("Chimamanda Adichie")
    author2 = Author.create("Ngũgĩ wa Thiong'o")
    author3 = Author.create("Wole Soyinka")

    mag1 = Magazine.create("African Literature Monthly", "Literature")
    mag2 = Magazine.create("Pan-African Tech", "Technology")

    Article.create("The Power of Storytelling", author1, mag1)
    Article.create("Decolonising the Mind", author2, mag1)
    Article.create("AI in Africa", author3, mag2)
    Article.create("The Digital Continent", author1, mag2)

if __name__ == "__main__":
    seed_data()
    print("Seed data inserted.")
