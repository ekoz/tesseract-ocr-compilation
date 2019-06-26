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
import subprocess
import os
from datetime import datetime
import time
from flask import Flask, request, render_template

UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 't4-res')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template('index.html')


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
    # the input device is not a TTY
    # https://stackoverflow.com/questions/43099116/error-the-input-device-is-not-a-tty
    # https://stackoverflow.com/questions/49724232/docker-compose-exec-python-the-input-device-is-not-a-tty-in-aws-ec2-userdata
    cmd_str = 'docker exec -i t4cmp tesseract ' + \
        tmp_file_dir + ' ' + tmp_file_dir + ' --oem 1 -l chi_sim'
    # method 1
    # os.system(cmd_str)
    print(cmd_str)
    # method 2
    p = subprocess.Popen(cmd_str, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    p.daemon = True
    output, errors = p.communicate()
    print(output)
    print(errors)
    # subprocess.call(cmd_str, shell=True)

    time.sleep(1)
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
