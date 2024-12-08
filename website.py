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
    return redirect("https://www.dropbox.com/scl/fi/id1ohdm353m4qahxu6gzg/Erika-Avila-Resume.pdf?rlkey=56n5a6cp91q33jejx8grm0e94&st=04f0k5ph&dl=0")


if __name__ == '__main__':
    app.run(debug=True)