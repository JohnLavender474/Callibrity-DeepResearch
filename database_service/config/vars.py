import os


POSTGRES_USER = os.getenv(
    "POSTGRES_USER",
    "root",
)

POSTGRES_PASSWORD = os.getenv(
    "POSTGRES_PASSWORD",
    "password",
)

POSTGRES_DB = os.getenv(
    "POSTGRES_DB",
    "deepresearch",
)

POSTGRES_HOST = os.getenv(
    "POSTGRES_HOST",
    "localhost",
)

POSTGRES_PORT = int(
    os.getenv(
        "POSTGRES_PORT",
        "5432",
    )
)

DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
