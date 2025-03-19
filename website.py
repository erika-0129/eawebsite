from flask import Flask, url_for, render_template, request, session, flash, redirect
import os
import sqlite3 as sql
import Encryption

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
    return redirect(
        "https://www.dropbox.com/scl/fi/rha1xx9mnmdqsfy67q89f/resume_erika_avila.pdf?rlkey=v7nw9wg2kzqripi5kiz9ahw9f&dl=0")


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


# Landing page to introduce the product. No log in yet.
@app.route("/allocate_landing")
def allocate_landing():
    return render_template('allocate_landing.html')


# Takes user to either log in page or home page after logged in
@app.route("/allocate_login_landing")
def allocate_login_landing():
    if not session.get('logged_in'):
        return render_template('allocate_login_landing.html')
    else:
        return render_template('allocate_logged_in.html', Name=session['U_Name'])


# Encrypts the login information, then checks it against the database to allow login access.
@app.route("/allocate_login", methods=["POST"])
def allocate_login():
    try:
        username = request.form['username']
        unm = str(Encryption.cipher.encrypt(bytes(username, 'utf-8')).decode("utf-8"))  # Encrypt information entered
        pwd = request.form['password']
        pwd = str(Encryption.cipher.encrypt(bytes(pwd, 'utf-8')).decode("utf-8"))  # Encrypt information entered

        # Call a sql database with name and password
        with sql.connect("customers.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()

            sql_select_query = """SELECT * FROM CustomerInfo WHERE U_Name = ? and Password = ?"""
            cur.execute(sql_select_query, (unm, pwd))

            row = cur.fetchone()
            if row is not None:
                session['logged_in'] = True
                session['U_Name'] = username
                session['userID'] = int(row['userID'])
            else:
                session['logged_in'] = False
                flash('Invalid username or password')
    except:
        con.rollback()
        flash('Error in insert operation')
    finally:
        con.close()
    return allocate_login_landing()

# Log out site
@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['U_Name'] = ""
    return allocate_landing()

# Landing site to add new users
@app.route("/allocate_new_user")
def new_user():
    if not session.get('logged_in'):
        return render_template('allocate_login_landing.html')
    else:
        return render_template('new_user.html')


# Add user to the database
@app.route("/addrecord", methods=['POST', 'GET'])
def addrecord():
    if not session.get('logged_in'):
        return allocate_landing()
    else:
        if request.method == 'POST':
            try:
                error = False
                fnm = request.form['First Name']
                lnm = request.form['Last Name']
                unm = request.form['Username']
                email = request.form['Email Address']
                phn = request.form['Phone Number']
                pw = request.form['Password']

                # Condition to check for empty spaces
                fnm = str(fnm).strip()
                lnm = str(lnm).strip()
                phn = str(phn).strip()
                unm = str(unm).strip()
                email = str(email).strip()
                pw = str(pw).strip()

                # Checks if name is present
                msg = "\n"
                if len(fnm) == 0:
                    error = True
                    msg += "Cannot add record. First Name is required. \n"
                if len(lnm) == 0:
                    error = True
                    msg += "Cannot add record. Last Name is required. \n"
                if len(email) == 0:
                    error = True
                    msg += "Cannot add record. Email is required. \n"
                if len(unm) == 0:
                    error = True
                    msg += "Cannot add record. Username is required. \n"
                if len(phn) == 0:
                    error = True
                    msg += "Cannot add an empty number. \n"
                if len(pw) == 0:
                    error = True
                    msg += "Must enter a password. \n"

                # Adding conditions to encrypt data
                fnm = str(Encryption.cipher.encrypt(bytes(fnm, 'utf-8')).decode("utf-8"))
                lnm = str(Encryption.cipher.encrypt(bytes(lnm, 'utf-8')).decode("utf-8"))
                email = str(Encryption.cipher.encrypt(bytes(email, 'utf-8')).decode("utf-8"))
                unm = str(Encryption.cipher.encrypt(bytes(unm, 'utf-8')).decode("utf-8"))
                phn = str(Encryption.cipher.encrypt(bytes(phn, 'utf-8')).decode("utf-8"))
                pw = str(Encryption.cipher.encrypt(bytes(pw, 'utf-8')).decode("utf-8"))

                # If all conditions above are met, we can add user info to the table
                if not error:
                    with sql.connect("customers.db") as con:
                        cur = con.cursor()

                        cur.execute(
                            "INSERT INTO CustomerInfo (F_Name, L_Name, U_Name, Email, Phone, Password) VALUES "
                            "(?,?,?, ?, ?, ?)", (fnm, lnm, unm, email, phn, pw))
                        con.commit()
                        msg = "Record successfully added"
            except:
                con.rollback()
                msg = "Error in insert operation"

            finally:
                return render_template("Results.html", msg=msg)
                con.close()


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
