from flask import Flask, render_template, request, redirect

app = Flask(__name__)

FILE_NAME = "users.txt"


def read_users():
    users = {}
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                email, password = line.strip().split(",")
                users[email] = password
    except FileNotFoundError:
        pass
    return users


def save_user(email, password):
    with open(FILE_NAME, "a") as file:
        file.write(f"{email},{password}\n")


@app.route('/')
def home():
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        users = read_users()

        if email in users:
            return "User already exists"

        save_user(email, password)
        return "Registration successful. Go to login."

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        users = read_users()

        if email in users and users[email] == password:
            return "Login successful"
        else:
            return "Invalid email or password"

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)