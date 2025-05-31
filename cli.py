from lib.models.author import Author
from lib.models.magazine import Magazine

def print_menu():
    print("\n==== Article Management CLI ====")
    print("1. Create Author")
    print("2. List Authors")
    print("3. Create Magazine")
    print("4. List Magazines")
    print("5. Add Article")
    print("6. List Articles by Author")
    print("7. List Articles in Magazine")
    print("8. List Magazine Contributors")
    print("9. Exit")

def create_author():
    name = input("Enter author name: ").strip()
    try:
        author = Author.create(name)
        print(f"Author '{author.name}' created with ID {author.id}.")
    except Exception as e:
        print(f"Error: {e}")

def list_authors():
    print("\n=== Authors ===")
    for id in range(1, 100):
        author = Author.find_by_id(id)
        if author:
            print(f"{author.id}. {author.name}")

def create_magazine():
    name = input("Magazine name: ").strip()
    category = input("Magazine category: ").strip()
    try:
        mag = Magazine.create(name, category)
        print(f"Magazine '{mag.name}' created with ID {mag.id}.")
    except Exception as e:
        print(f"Error: {e}")

def list_magazines():
    print("\n=== Magazines ===")
    for id in range(1, 100):
        mag = Magazine.find_by_id(id)
        if mag:
            print(f"{mag.id}. {mag.name} ({mag.category})")

def add_article():
    list_authors()
    aid = input("Author ID: ").strip()
    list_magazines()
    mid = input("Magazine ID: ").strip()
    title = input("Article title: ").strip()
    try:
        author = Author.find_by_id(int(aid))
        mag = Magazine.find_by_id(int(mid))
        if not author or not mag:
            raise ValueError("Invalid author or magazine ID.")
        article = author.add_article(mag, title)
        print(f"Article '{article.title}' created with ID {article.id}.")
    except Exception as e:
        print(f"Error: {e}")

def list_articles_by_author():
    list_authors()
    aid = input("Enter Author ID: ").strip()
    try:
        author = Author.find_by_id(int(aid))
        if author:
            articles = author.articles()
            print(f"\nArticles by {author.name}:")
            for article in articles:
                print(f"- {article.title}")
        else:
            print("Author not found.")
    except Exception as e:
        print(f"Error: {e}")

def list_articles_in_magazine():
    list_magazines()
    mid = input("Enter Magazine ID: ").strip()
    try:
        mag = Magazine.find_by_id(int(mid))
        if mag:
            articles = mag.articles()
            print(f"\nArticles in {mag.name}:")
            for article in articles:
                print(f"- {article.title}")
        else:
            print("Magazine not found.")
    except Exception as e:
        print(f"Error: {e}")

def list_contributors():
    list_magazines()
    mid = input("Enter Magazine ID: ").strip()
    try:
        mag = Magazine.find_by_id(int(mid))
        if mag:
            contributors = mag.contributors()
            print(f"\nContributors to {mag.name}:")
            for contributor in contributors:
                print(f"- {contributor.name}")
        else:
            print("Magazine not found.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    while True:
        print_menu()
        choice = input("Choose an option (1-9): ").strip()
        if choice == "1":
            create_author()
        elif choice == "2":
            list_authors()
        elif choice == "3":
            create_magazine()
        elif choice == "4":
            list_magazines()
        elif choice == "5":
            add_article()
        elif choice == "6":
            list_articles_by_author()
        elif choice == "7":
            list_articles_in_magazine()
        elif choice == "8":
            list_contributors()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-9.")

if __name__ == "__main__":
    main()
