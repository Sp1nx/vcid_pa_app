from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Verbindung zur MySQL-Datenbank herstellen
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Samira-01",
    database="personal"
)
cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

#@app.route('/')
#def index():
#    return send_from_directory('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Benutzer in die MySQL-Datenbank einfügen
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()  # Änderungen in der Datenbank speichern

        return redirect(url_for('dashboard'))

    return render_template('index.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        loginusername = request.form['loginusername']
        loginpassword = request.form['loginpassword']

        # Überprüfen, ob der Benutzer in der Datenbank existiert
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid login'

    return render_template('index')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index.html'))

if __name__ == '__main__':
    app.run(debug=True)


