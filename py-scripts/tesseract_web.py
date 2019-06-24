#!/usr/bin/env python
# encoding: utf-8

"""
$env:FLASK_APP="tesseract_web.py"
flask run
@version: 1.0
@author: eko.zhan
@contact: eko.z@hotmail.com
@file: tesseract_web.py
@time: 2019/6/24 10:55
@see https://docs.python.org/3/library/tempfile.html
@see http://flask.pocoo.org/docs/1.0/
"""
import argparse
import tempfile
import os
from datetime import datetime
from flask import Flask, request

UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 't4-res')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index():
    return "It works."


@app.route('/upload', methods=['post'])
def upload():
    f = request.files['file']
    if not allowed_file(f.filename):
        return '-1'
    # filename
    filename = datetime.now().isoformat('_') + '.' + get_file_suffix(f.filename)
    # get img file path
    tmp_file_dir = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # save img into tmp dir
    f.save(tmp_file_dir)
    # use tesseract-ocr
    os.system(
        'docker exec -it t4cmp tesseract ' + tmp_file_dir + ' ' + tmp_file_dir + ' --oem 1 -l chi_sim')
    with open(tmp_file_dir + '.txt') as file_obj:
        return file_obj.read()
    return ''


def allowed_file(filename):
    return '.' in filename and \
           get_file_suffix(filename) in ALLOWED_EXTENSIONS


def get_file_suffix(filename):
    return filename.rsplit('.', 1)[1].lower()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    app.run(host=args.host, port=args.port)
