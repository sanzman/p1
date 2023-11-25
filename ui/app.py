from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a random key for session management

@app.route('/')
def home():
    session['number'] = random.randint(1, 100)  # Store the random number in session
    session['attempts'] = 0
    return render_template('index.html')  # Create this template

@app.route('/guess', methods=['POST'])
def guess():
    guess = int(request.form['guess'])
    session['attempts'] += 1

    if guess < session['number']:
        message = "Too low!"
    elif guess > session['number']:
        message = "Too high!"
    else:
        message = f"Congratulations! You guessed the number in {session['attempts']} attempts."
        return render_template('index.html', message=message, game_over=True)

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
