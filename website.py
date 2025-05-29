from flask import Flask, render_template, request, session, redirect
import os


app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

"""
EA Portfolio Main Page
"""
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
    return redirect(
        "https://www.dropbox.com/scl/fi/r7qudm8phg6jlofrwom2l/resume_erika_avila.pdf?rlkey=1ix6d8imz5d6c43lnjlttq413&dl=0")

@app.route("/certifications")
def certifications():
    return render_template('certifications.html')


"""
For Valentines Day Website
"""
@app.route("/valentines")
def valentine():
    if request.method == "POST":
        session['answers'] = request.form.to_dict()
        return render_template("valentines_responses.html", answers=session['answers'])
    return render_template("valentines.html")

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
