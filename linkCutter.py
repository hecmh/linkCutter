from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

@app.before_request
def create_table():
    db.create_all()

# Модель для базы данных
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500))
    short_url = db.Column(db.String(10), unique=True)

    def __init__(self, original_url, short_url):
        self.original_url = original_url
        self.short_url = short_url

# Главная страница
@app.route('/')
def home():
    return render_template('home.html')

# Код для создания короткой ссылки
@app.route('/shorten_url', methods=['POST'])
def shorten_url():
    original_url = request.form['original_url']
    chars = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(chars) for i in range(7))
    new_url = URL(original_url=original_url, short_url=short_url)
    db.session.add(new_url)
    db.session.commit()
    return render_template('shortened.html', short_url=short_url)

# Перенаправление пользователя по короткой ссылке
@app.route('/<short_url>')
def redirect_short_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first_or_404()
    return redirect(url.original_url)

if __name__ == '__main__':
    app.run(debug=True)