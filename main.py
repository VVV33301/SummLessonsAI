from flask import Flask, request, jsonify
from requests import get
from sqlalchemy import create_engine, Column, Integer, String, Boolean, select
from sqlalchemy.orm import DeclarativeBase, Session
import urllib.parse
from subprocess import call
import json
from time import time
from typing import Iterable, List

from models import *

YANDEX_DISK_URL = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'


class Tokens(DeclarativeBase):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    token = Column(String, unique=True, nullable=False)
    is_paid = Column(Boolean, nullable=False, default=False)


app = Flask(__name__)
tokens_engine = create_engine('sqlite:///tokens.db')
Tokens.metadata.create_all(tokens_engine)


def check_token(token):
    with Session(tokens_engine) as session:
        return bool(Tokens.query.filter_by(token=token).first())


def yandex_disk_download(url):
    final_url = YANDEX_DISK_URL + urllib.parse.urlencode(dict(public_key=url))
    response = get(final_url)
    download_url = response.json()['href']

    download_response = get(download_url)
    filename = f'downloads/y_audio_{time()}.{download_url.rsplit(".")[-1]}'
    with open(filename, 'wb') as f:
        f.write(download_response.content)
    return filename


@app.route('/<string:token>/summarize-text', methods=['GET'])
def get_from_text(token):
    if check_token(token):
        if request.args['text']:
            print(res := summarize_text(urllib.parse.unquote(request.args['text'])))
            return res, 200
        return 'Request has not contain text', 400
    return 'Unexpected token', 403


@app.route('/<string:token>/from-yadisk', methods=['GET'])
def get_from_text(token):
    if check_token(token):
        if request.args['link']:
            file = yandex_disk_download(urllib.parse.unquote(request.args['link']))
            text = tokenize_audio(file)
            print(res := summarize_text(text))
            return res, 200
        return 'Request has not contain link to Yandex Disk', 400
    return 'Unexpected token', 403


@app.route('/<string:token>/from-file', methods=['GET'])
def get_from_text(token):
    if check_token(token):
        print(res := summarize_text(urllib.parse.unquote(request.args['text'])))
        return res, 200
    return 'Unexpected token', 403


@app.route('/<string:token>/from-url', methods=['GET'])
def get_from_text(token):
    if check_token(token):
        print(res := summarize_text(urllib.parse.unquote(request.args['text'])))
        return res, 200
    return 'Unexpected token', 403


if __name__ == '__main__':
    app.run(debug=True)