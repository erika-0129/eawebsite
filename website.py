from flask import Flask, url_for, render_template, request, session, flash, redirect
import os
import sqlite3 as sql
import Encryption
import pandas as pd
from bcrypt import hashpw, gensalt, checkpw

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

"""AlloCredit Website"""

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
        return render_template('allocate_logged_in.html', Name=session['F_Name'])


# Encrypts the login information, then checks it against the database to allow login access.
@app.route("/allocate_login", methods=["POST"])
def allocate_login():
    try:
        username = request.form['username']
        encrypted_username = str(Encryption.cipher.encrypt(bytes(username, 'utf-8')).decode("utf-8"))  # Encrypt information entered
        pwd = request.form['password']
        encrypted_password = str(Encryption.cipher.encrypt(bytes(pwd, 'utf-8')).decode("utf-8"))  # Encrypt information entered

        # Call a sql database with name and password
        with sql.connect("customers.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()

            sql_select_query = """SELECT * FROM CustomerInfo WHERE U_Name = ? and Password = ?"""
            cur.execute(sql_select_query, (encrypted_username, encrypted_password))

            row = cur.fetchone()
            if row is not None:
                session['logged_in'] = True
                session['U_Name'] = username
                session['userID'] = int(row['userID'])
                session['F_Name'] = str(Encryption.cipher.decrypt(row['F_Name']))
                if int(row['AdminLevel']) == 1:
                    session['admin1'] = True
                elif int(row['AdminLevel']) == 2:
                    session['admin2'] = True
                elif int(row['AdminLevel']) == 3:
                    session['admin3'] = True
                else:
                    session['admin1'] = False
                    session['admin2'] = False
                    session['admin3'] = False
            else:
                session['logged_in'] = False
                flash('Invalid username or password')
    except Exception as e:
        con.rollback()
        flash(f'Error: {str(e)}')
    finally:
        con.close()
    return allocate_login_landing()

# Log out site
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('allocate_landing'))

# For admins to create a new account
@app.route("/allocate_new_user")
def new_user():
    if not session.get('logged_in'):
        return render_template('allocate_login_landing.html')
    else:
        return render_template('new_user.html')

# For when new users want to create an account
@app.route("/create_account")
def create_new_account():
    return render_template('new_user.html')

# Site that redirects after user attempts to enter a record.
@app.route('/Results', methods=['GET', 'POST'])
def results():
    if not session.get('logged_in'):
        return render_template('allocate_login_landing.html')
    elif session.get('admin1') is True:
        if request.method == 'POST':
            return render_template('Results.html')

# Add user to the database
@app.route("/addrecord", methods=['POST', 'GET'])
def addrecord():
    if not session.get('logged_in'):
        return allocate_landing()
    elif session.get('admin1') is True:
        if request.method == 'POST':
            try:
                error = False
                fnm = request.form['F_Name']
                lnm = request.form['L_Name']
                unm = request.form['U_Name']
                email = request.form['Email']
                phn = request.form['Phone']
                pw = hashpw(request.form['Password'].encode('utf-8'), gensalt())

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
                #pw = str(Encryption.cipher.encrypt(bytes(pw, 'utf-8')).decode("utf-8"))

                # If all conditions above are met, we can add user info to the table
                try:
                    with sql.connect("customers.db") as con:
                        cur = con.cursor()

                        cur.execute(
                            "INSERT INTO CustomerInfo (F_Name, L_Name, U_Name, AdminLevel, Email, Phone, Password) VALUES "
                            "(?, ?, ?, ?, ?, ?, ?)", (fnm, lnm, unm, 3, email, phn, pw))
                        con.commit()
                        msg = "Record successfully added"
                except Exception as e:
                    con.rollback()
                    msg = f"Error in insert operation: {str(e)}"
            except:
                con.rollback()
                msg = "Error in insert operation"

            finally:
                return render_template("Results.html", msg=msg)
                con.close()

# View current users
@app.route('/CurrentUsers')
def currentusers():
    if not session.get('logged_in'):
        return render_template('allocate_login_landing.html')
    elif session.get('admin1') is True:
        con = sql.connect("customers.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("SELECT F_Name, L_Name, U_Name, Email, Phone FROM CustomerInfo")
        df = pd.DataFrame(cur.fetchall(), columns=['First Name', 'Last Name', 'Username', 'Email', 'Phone Number'])

        # Converting to an array and decrypting
        index = 0
        for fnm in df['First Name']:
            fnm = str(Encryption.cipher.decrypt(fnm))
            df._set_value(index, 'First Name', fnm)
            index += 1
        index = 0
        for lnm in df['Last Name']:
            lnm = str(Encryption.cipher.decrypt(lnm))
            df._set_value(index, 'Last Name', lnm)
            index += 1
        index = 0
        for unm in df['Username']:
            unm = str(Encryption.cipher.decrypt(unm))
            df._set_value(index, 'Username', unm)
            index += 1
        index = 0
        for email in df['Email']:
            email = str(Encryption.cipher.decrypt(email))
            df._set_value(index, 'Email', email)
            index += 1
        index = 0
        for phn in df['Phone Number']:
            phn = str(Encryption.cipher.decrypt(phn))
            df._set_value(index, 'Phone Number', phn)
            index += 1

        con.close()

        return render_template("current_users.html", rows=df)
    else:
        return render_template('allocate_login_landing.html')

@app.route('/ShowUserInfo')
def showuser():
    if not session.get('logged_in'):
        return render_template("allocate_login_landing.html")
    else:
        con = sql.connect("customers.db")
        con.row_factory = sql.Row
        cur = con.cursor()

        search_username = Encryption.cipher.encrypt(bytes(session['U_Name'], 'utf-8')).decode("utf-8")
        sql_select_query = """SELECT F_Name, L_Name, U_Name, AdminLevel, Email, Phone FROM CustomerInfo WHERE 
        U_Name = ?"""

        cur.execute(sql_select_query, [search_username])

        data = cur.fetchall()
        if not data:
            flash("No user information found")

        df = pd.DataFrame(data, columns=['First Name', 'Last Name', 'User Name', 'Admin Level', 'Email', 'Phone'])

        # Decrypt fields before displaying
        decrypt = lambda x: Encryption.cipher.decrypt(x.encode("utf-8"))
        df['First Name'] = df['First Name'].apply(decrypt)
        df['Last Name'] = df['Last Name'].apply(decrypt)
        df['User Name'] = df['User Name'].apply(decrypt)
        df['Email'] = df['Email'].apply(decrypt)
        df['Phone'] = df['Phone'].apply(decrypt)

        con.close()

        return render_template("AppUser.html", row=df)

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
