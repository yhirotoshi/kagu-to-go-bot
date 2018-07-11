from flask import Flask, request, abort
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from settings import *

# TODO Base.pyに置くとエラるのでとりあえずここにあるけど移設する方法考える
class User(Base): # 追加
    __tablename__ = "users" # 追加
    __table_args__ = {'extend_existing': True}
    uid =Column(String(150), primary_key=True) # 追加
    slack_id =Column(String(150), nullable=False)
    channel_id = Column(String(150), nullable=False)
    created_at = Column(DateTime, nullable=False) # 追加

class Chat_log(Base): # 追加
    __tablename__ = "chat_logs" # 追加
    __table_args__ = {'extend_existing': True}
    uid =Column(String(150),  primary_key=True) # 追加
    created_at =Column(DateTime, nullable=False) # 追加
    message = Column(String(150), nullable=False) # 追加
    message_type = Column(String(150), nullable=True)


Base.metadata.create_all(ENGINE)
