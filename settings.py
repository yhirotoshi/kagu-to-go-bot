import os
from os.path import join, dirname
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
dotenv_path = join(dirname(__file__),'test.env')
load_dotenv(dotenv_path)

channel_secret = os.environ.get('LINE_CHANNEL_SECRET')
channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
WEB_HOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')
SLACK_BOT_TOKEN=os.environ.get('SLACK_BOT_TOKEN')
SLACK_API_TOKEN=os.environ.get('SLACK_API_TOKEN')
DB_URI=os.environ.get('DB_URI')

ENGINE = create_engine(
    DB_URI,
    encoding = "utf-8",
    echo=True # Trueだと実行のたびにSQLが出力される
)

# Sessionの作成
session = scoped_session(
  # ORM実行時の設定。自動コミットするか、自動反映するなど。
        sessionmaker(
                autocommit = False,
                autoflush = False,
                bind = ENGINE
        )
)

Base = declarative_base()
