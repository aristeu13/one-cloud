from app.core.settings.client import client


def get_db():
    db = client["onecloud"]
    return db
