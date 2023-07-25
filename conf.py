from envparse import Env

env = Env()


REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres:maksikos973@localhost:5432/postgres",          
)