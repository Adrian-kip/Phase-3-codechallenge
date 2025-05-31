import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

def setup_function(function):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()

def test_create_and_find_author():
    author = Author.create("Test Author")
    found = Author.find_by_id(author.id)
    assert found is not None
    assert found.name == "Test Author"

def test_author_articles_and_magazines():
    author = Author.create("Alice")
    magazine = Magazine.create("Tech Today", "Technology")
    article = author.add_article(magazine, "Future Tech")

    articles = author.articles()
    assert len(articles) == 1
    assert articles[0].title == "Future Tech"

    magazines = author.magazines()
    assert any(m.name == "Tech Today" for m in magazines)

def test_magazine_contributors_and_articles():
    author1 = Author.create("Bob")
    author2 = Author.create("Carol")
    magazine = Magazine.create("Health Weekly", "Health")
    author1.add_article(magazine, "Health Tips")
    author2.add_article(magazine, "Nutrition Guide")

    contributors = magazine.contributors()
    assert len(contributors) >= 2

    titles = magazine.article_titles()
    assert "Health Tips" in titles
    assert "Nutrition Guide" in titles

def test_article_author_and_magazine():
    author = Author.create("Dan")
    magazine = Magazine.create("Sports Monthly", "Sports")
    article = Article.create("Championship Highlights", author, magazine)
    assert article.author().name == "Dan"
    assert article.magazine().name == "Sports Monthly"
