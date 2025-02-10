from flask import Flask, url_for, render_template, request, session, flash, redirect
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/projects")
def projects():
    return render_template('projects.html')

@app.route("/resume")
def resume():
    return redirect("https://www.dropbox.com/scl/fi/rha1xx9mnmdqsfy67q89f/resume_erika_avila.pdf?rlkey=v7nw9wg2kzqripi5kiz9ahw9f&dl=0")

@app.route("/certifications")
def certifications():
    return render_template('certifications.html')

@app.route("/valentines")
def valentine():
    return render_template('valentines.html')

if __name__ == '__main__':
    app.run(debug=True)