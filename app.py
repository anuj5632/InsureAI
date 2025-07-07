from flask import Flask, render_template, request, redirect, url_for, session
import joblib  
import numpy as np

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Load the trained model
model = joblib.load('insurance_model.pkl')  
users = {}

@app.route('/')
def cover():
    return render_template('cover.html')

@app.route('/about')
def about():
    return render_template('about.html')  


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('signup.html', error="Username already exists.")
        users[username] = password
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials.")
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user' not in session:
        return redirect(url_for('login'))

    prediction = None

    if request.method == 'POST':
        try:
            age = float(request.form['age'])
            bmi = float(request.form['bmi'])
            children = int(request.form['children'])
            smoker = 1 if request.form['smoker'] == 'yes' else 0
            sex = 1 if request.form['sex'] == 'male' else 0
            region = int(request.form['region'])

            input_data = np.array([[age, bmi, children, smoker, sex, region]])
            prediction = model.predict(input_data)[0]
            prediction = round(prediction, 2)
        except Exception as e:
            prediction = f"Error: {e}"

    return render_template('index.html', prediction=prediction)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
