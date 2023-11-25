from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a random key for session management

@app.route('/')
def home():
    # Default difficulty to medium if not set
    if 'number' not in session:
        session['number'] = random.randint(1, 100)
        session['attempts'] = 0
        session['guesses'] = []
    return render_template('index.html')

@app.route('/set_difficulty', methods=['POST'])
def set_difficulty():
    difficulty = request.form['difficulty']
    print("Difficulty:", difficulty)
    if difficulty == 'easy':
        session['number'] = random.randint(1, 50)
    elif difficulty == 'hard':
        session['number'] = random.randint(1, 200)
    else:  # medium
        session['number'] = random.randint(1, 100)
    
    session['attempts'] = 0
    session['guesses'] = []
    return redirect(url_for('home'))

@app.route('/guess', methods=['POST'])
def guess():
    guess = int(request.form['guess'])
    session['attempts'] += 1
    session['guesses'].append(guess)

    if guess < session['number']:
        message = "Too low!"
    elif guess > session['number']:
        message = "Too high!"
    else:
        message = f"Congratulations! You guessed the number in {session['attempts']} attempts."
        return render_template('index.html', message=message, game_over=True, guesses=session['guesses'])

    if session['attempts'] == 7:
        message = f"You ran out of attempts! Game over! The number was {session['number']}."
        return render_template('index.html', message=message, game_over=True, guesses=session['guesses'])

    return render_template('index.html', message=message, guesses=session['guesses'])

if __name__ == '__main__':
    app.run(debug=True)
