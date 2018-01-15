import os

from flask import Flask, request, Response, jsonify, json
from flask import render_template, url_for, redirect, send_from_directory
from flask import make_response, abort, session

from project import app
from project.core import db
from project.models import *

from project.face_detect import FaceDetect

@app.route('/')
def index():
    return render_template('index.html', title="Home")

@app.route('/main_detect/')
def main():
    return render_template('main.html', title="Deteksi Ekspresi")

@app.route('/detect_result/')
def detect_result():
    return render_template('detect_result.html', title="Hasil Deteksi Ekspresi")

def generate(detect):
    while True:
        frame = detect.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/feed_stream/')
def feed_stream():
    return Response(generate(FaceDetect()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/photos/')
def photos():
    return render_template('photos.html', title="Foto Percobaan")

@app.route('/results/')
def result():
    return render_template('results.html', title="Hasil Percobaan")

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            user = Admin.query.filter_by(username=username, password=password).first()
            if user is not None:
                return redirect('/admin/')
            else:
                return render_template('login.html', title="Login Admin")
        except:
            return 'error query'
    return render_template('login.html', title="Login Admin")

@app.route('/admin/')
def admin():
    return render_template('admin.html', title="Admin Page")