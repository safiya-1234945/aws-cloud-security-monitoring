import os


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


DATABASE_FOLDER = os.path.join(
    BASE_DIR,
    "database"
)


PRODUCTION_DATABASE = os.path.join(
    DATABASE_FOLDER,
    "production.db"
)


EVALUATION_DATABASE = os.path.join(
    DATABASE_FOLDER,
    "evaluation.db"
)