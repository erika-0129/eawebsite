import sqlite3
import Encryption
import random

# Create Database
conn = sqlite3.connect('customers.db')

# Cursor to execute queries
cur = conn.cursor()

# Drop table from database
try:
    conn.execute('''Drop table CustomerInfo''')
    conn.commit()
    print("CustomerInfo Table Dropped")
except:
    print("CustomerInfo table did not exist")

# Create Customer info table
cur.execute('''CREATE TABLE CustomerInfo(
userId INTEGER PRIMARY KEY NOT NULL,
F_Name TEXT NOT NULL,
L_Name TEXT NOT NULL,
U_Name TEXT NOT NULL,
AdminLevel INT,
Email TEXT NOT NULL,
Phone TEXT NOT NULL,
Password TEXT NOT NULL);
''')
conn.commit()
print("CustomerInfo table created")

rand_userID = random.randint(100, 1000)

# EA Account
fnm = str(Encryption.cipher.encrypt(b'Erika').decode("utf-8"))
lnm = str(Encryption.cipher.encrypt(b'Avila').decode("utf-8"))
unm = str(Encryption.cipher.encrypt(b'eavila').decode("utf-8"))
pwd = str(Encryption.cipher.encrypt(b'1234').decode("utf-8"))
email = str(Encryption.cipher.encrypt(b'erika12994@gmail.com').decode("utf-8"))
phn = str(Encryption.cipher.encrypt(b'123-123-1234').decode("utf-8"))
cur.execute("INSERT INTO CustomerInfo (F_Name, L_Name, U_Name, AdminLevel, Email, Phone, Password) VALUES(?, ?, ?, ?, ?, ?, ?)",
            (fnm, lnm, unm, 1, email, phn, pwd))
conn.commit()

# Show table. Iterate rows
for row in cur.execute('SELECT * FROM CustomerInfo;'):
    print(row)

# Close database connection
conn.close()
print("Connection Closed")