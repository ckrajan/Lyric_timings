import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template, make_response
from werkzeug.utils import secure_filename
import csv
import os
import shutil
from pydub import AudioSegment

import fnmatch
from collections import defaultdict
import json

if not os.path.exists('static/uploads'):
	os.makedirs('static/uploads/', exist_ok=True)

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__, static_url_path='/static')
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route("/")
def cutter():
    return render_template('cutter.html')

@app.route('/compare')
def compare_tool():
    return render_template('compare.html')


@app.route('/', methods=['POST'])
def upload_video():
	collection = request.form.get('collection')
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	else:
		filename = secure_filename(file.filename)
		filename_only = os.path.splitext(filename)[0]

		if not os.path.exists('static/uploads/%s' % filename_only + '/'):
			os.makedirs('static/uploads/%s' % filename_only + '/', exist_ok=True)

		file.save(os.path.join('static/uploads/%s' % filename_only + '/', filename))
		flash('Audio successfully uploaded')
		return render_template('cutter.html', filename=filename, collection=collection)

@app.route('/upload_csv', methods=['POST'])
def upload():
	json_body = request.get_json()
	csv_str = json_body['csv']
	filename = json_body['filename']
	filename_only = os.path.splitext(filename)[0]

	reader = csv.reader(csv_str.splitlines(), skipinitialspace=True)
	with open('static/uploads/%s' % filename_only + '/' + filename_only + '.csv', 'w') as out_file:
		writer = csv.writer(out_file)
		writer.writerows(reader)


@app.route('/display/<filename>')
def display_video(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/uploaded_files', methods=['GET', 'POST'])
def uploaded_files():
	video_list = 'static/uploads/'
	allfiles = os.listdir(video_list)
	files = [ fname for fname in allfiles ]
	return files


if __name__ == '__main__':
    app.run(port=8080, debug=True)