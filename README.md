<img width="1683" height="947" alt="Screenshot 2026-05-15 145005" src="https://github.com/user-attachments/assets/f4c9bd59-8ba2-48fb-b291-ea30d6bf78a9" />

# BrainJar

BrainJar is a lightweight Django notes app for tracking topics, progress notes, and tags. It provides user registration and authentication, topic management, session logging, and lightweight tag organization.

## Features

- User signup, login, and logout
- Create, edit, and delete Topics
- Track topic status with Not Started / In Progress / Completed
- Add progress Notes to each Topic
- Add Notes with date, content, and optional reference details
- Create and reuse Tags across topics
- View Topics by Tags and see tag counts
- Responsive templates with a simple, clean UI
- Heroku-compatible deployment via `Procfile`

- ## Tech Stack

- Python 3.11
- Django 5.2
- PostgreSQL
- Whitenoise for static file delivery
- Gunicorn for WSGI production hosting
- python-dotenv for environment variable loading
- dj-database-url for Heroku database parsing

- ## Models

- `Topic`: user-owned topic with name, description, status, and tags
- `Tag`: user-owned tag name, scoped per user
- `Note`: dated progress note attached to a topic with optional reference text
