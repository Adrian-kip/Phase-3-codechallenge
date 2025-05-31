from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

a = Author.create("Adrian")
m = Magazine.create("Tech Weekly", "Technology")

Article.create("How AI is Changing Africa", a.id, m.id)
