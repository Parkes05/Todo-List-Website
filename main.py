from flask import Flask, render_template, redirect, url_for, flash, request
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_bootstrap import Bootstrap5
from forms import *
from flask_login import LoginManager, login_user, logout_user, UserMixin, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
Bootstrap5(app)
ckeditor = CKEditor(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', 'sqlite:///my_user.db')
db = SQLAlchemy(app)

login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(id):
    return db.get_or_404(User, id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    list = relationship('List', back_populates='user')

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = relationship('User', back_populates='list')


with app.app_context():
    db.create_all()

def current_dt():
    dt = datetime.now()
    date = dt.strftime('%B, %Y')
    return date


@app.route('/', methods=['GET', 'POST'])
def home():
    reg_form = Register()
    if reg_form.validate_on_submit():
        name = reg_form.name.data
        email = reg_form.email.data
        password = generate_password_hash(reg_form.password.data)
        new_user = User (
            name=name,
            email=email,
            password=password
        )
        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            flash('Email already exists. Try again or Login')
        else:
            login_user(new_user)
            return redirect(url_for('list'))
    if current_user.is_authenticated:
        return redirect(url_for('list'))
    return render_template('home.html', date=current_dt(), form=reg_form, login=False)


@app.route('/register')
def register():
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    log_form = Login()
    if log_form.validate_on_submit():
        email = log_form.email.data
        check = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if check == None:
            flash('Email doesn\'t exist, try again')
            return render_template('login.html', date=current_dt(), login=True, form=log_form, show=True)
        if check_password_hash(check.password, log_form.password.data):
            login_user(check)
            return redirect(url_for('list'))
        else:
            flash('Incorrect password, try again')
            return render_template('login.html', date=current_dt(), login=True, form=log_form, show=True)
    return render_template('login.html', date=current_dt(), login=True, form=log_form, show=True)


@app.route('/list', methods=['GET', 'POST'])
@login_required
def list():
    if request.method == 'POST':
        new_list = List(
            title = request.form['title'],
            user_id = current_user.id
        )
        db.session.add(new_list)
        db.session.commit()
    my_list = db.session.execute(db.select(List).where(List.user_id == current_user.id)).scalars().all()
    return render_template('list.html', date=current_dt(), login=True, user=True, list=my_list)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/save', methods=['POST'])
@login_required
def save():
    title = [int(item) for item in request.form['title']]
    to_del = db.session.execute(db.select(List).where(List.user_id == current_user.id)).scalars().all()
    for i in to_del:
        if i.id not in title:
            entry_to_del = db.get_or_404(List, i.id)
            db.session.delete(entry_to_del)
            db.session.commit()
    return redirect(url_for('list'))
    


@app.route('/details/<title>', methods=['GET', 'POST'])
@login_required
def details(title):
    items = Items()
    real = db.session.execute(db.select(List).where(List.id == title)).scalar()
    if items.validate_on_submit() or request.method == 'POST':
        new_items = items.list_items.data
        if new_items == None:
            new_items = request.form['ckeditor']
        update = db.session.execute(db.select(List).where(List.id == title)).scalar()
        update.description = new_items
        db.session.commit()
        return redirect(url_for('list'))
    return render_template('details.html', title=real.title, form=items, new=real.description, id=real.id)





if __name__ == '__main__':
    app.run(debug=True)