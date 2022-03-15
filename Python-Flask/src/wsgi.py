from app import app

if __name__ == "__main__":
    app.run()

    # Run success on ubuntu 20 [wsl]
    # pip install gunicorn
    # (project1venv) $ gunicorn --bind 0.0.0.0:5000 wsgi:app
    