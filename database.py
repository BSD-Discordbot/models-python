import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import re
import os

url_tokens = {
        "DB_USER": os.getenv("DB_USER", ""),
        "DB_PASS": os.getenv("DB_PASS", ""),
        "DB_HOST": os.getenv("DB_HOST", ""),
        "DB_NAME": os.getenv("DB_NAME", "")
    }

url = 'postgresql://${DB_USER}:${DB_PASS}@${DB_HOST}/${DB_NAME}'

url = re.sub(r"\${(.+?)}", lambda m: url_tokens[m.group(1)], url)

connectable = create_engine(url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connectable)

Base = declarative_base()
