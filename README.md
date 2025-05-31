# Articles CLI App

This is a command-line application for managing authors, magazines, and articles using Python and raw SQL with SQLite3. It was built as part of the Flatiron School Phase 3 Code Challenge and demonstrates core principles of object-oriented programming, custom ORM methods, and database interaction without using frameworks like SQLAlchemy or Django.

## Overview

The app allows users to:

- Create authors and magazines
- Add articles that link authors to magazines
- View existing authors, magazines, and articles
- Explore relationships (such as all articles by an author or all contributors to a magazine)

The application uses raw SQL for all database interactions and Python classes to represent models.

## Features

- Create and view authors, magazines, and articles
- One-to-many relationships:
  - An author can write many articles
  - A magazine can have many articles
- Simple and intuitive CLI interface
- Input validation to ensure clean data entry
- Raw SQL queries used directly with SQLite3
- Includes test coverage using pytest

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/articles-cli-app.git
cd articles-cli-app

sqlite3 articles.db < lib/db/schema.sql

python lib/cli.py

pytest

pip install pytest
