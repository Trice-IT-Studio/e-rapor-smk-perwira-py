from flask import Blueprint, render_template, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Account
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/', methods=["GET"])
def login():
    return render_template('/auth/login.html')

@auth.route('/login', methods=['POST'])
def handle_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Account.query.filter(Account.username == username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                print('Login is successfull!')
                flash('Login berhasil, selamat datang.', category='success')
                return redirect(url_for('views.beranda'))
        else:
            print('Login is FAILED!!')
            flash('Gagal login, cek username dan password yang anda masukkan', category='error')
            return redirect(url_for('auth.login'))

    flash('Gagal login, cek username dan password yang anda masukkan', category='error')
    return redirect(url_for('auth.login'))


@auth.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
