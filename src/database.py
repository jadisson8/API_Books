from sqlmodel import create_engine
from decouple import config


def get_engine():
  user = config('DB_USERNAME')
  password = config('DB_PASSWORD')
  db_name = config('DB_NAME')
  host = config('DB_HOST')
  port = config('DB_PORT')
  return create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
