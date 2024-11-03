from flask import Flask, request, jsonify
from requests import get
from sqlalchemy import create_engine, Column, Integer, String, Boolean, select
from sqlalchemy.orm import DeclarativeBase, Session
from urllib.parse import urlencode, unquote
from urllib.request import urlretrieve
from subprocess import call
import json
from time import time

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
    final_url = YANDEX_DISK_URL + urlencode(dict(public_key=url))
    response = get(final_url)
    download_url = response.json()['href']

    download_response = get(download_url)
    filename = f'downloads/y_audio_{time()}.{download_url.rsplit(".")[-1]}'
    with open(filename, 'wb') as f:
        f.write(download_response.content)
    return filename


def url_download(url):
    filename = f'downloads/audio_{time()}.{url.rsplit(".")[-1]}'
    urlretrieve(url, filename)
    return filename


@app.route('/<string:token>/summarize-text', methods=['GET'])
def get_from_text(token):
    if check_token(token):
        if request.args['text']:
            print(res := summarize_text(unquote(request.args['text'])))
            return res, 200
        return 'Request has not contain text', 400
    return 'Unexpected token', 403


@app.route('/<string:token>/from-yadisk', methods=['GET'])
def get_from_text(token):
    if check_token(token):
        if request.args['link']:
            file = yandex_disk_download(unquote(request.args['link']))
            text = tokenize_audio(file)
            print(res := summarize_text(text))
            return res, 200
        return 'Request has not contain link to Yandex Disk', 400
    return 'Unexpected token', 403


@app.route('/<string:token>/from-file', methods=['POST'])
def get_from_text(token):
    if check_token(token):
        if request.args['c']:
            file = request.files['file']
            filename = f'download/{file.filename}'
            file.save(filename)
            text = tokenize_audio(filename)
            print(res := summarize_text(text))
            return res, 200
        return 'Request has not contain file', 400
    return 'Unexpected token', 403


@app.route('/<string:token>/from-url', methods=['GET'])
def get_from_text(token):
    if check_token(token):
        if request.args['link']:
            file = url_download(unquote(request.args['link']))
            text = tokenize_audio(file)
            print(res := summarize_text(text))
            return res, 200
        return 'Request has not contain link to file', 400
    return 'Unexpected token', 403


if __name__ == '__main__':
    app.run(debug=True)