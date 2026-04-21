from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth_bp
from app.models import User

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.get_by_username(username):
            flash('此帳號已被使用！', 'danger')
        elif User.get_by_email(email):
            flash('此信箱已被註冊！', 'danger')
        else:
            # 雜湊密碼以加強安全性
            password_hash = generate_password_hash(password)
            user = User.create(username, email, password_hash)
            if user:
                flash('註冊成功！麻煩請在此登入以啟用您的帳號。', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('註冊失敗，系統發生未知的錯誤，請重試。', 'danger')
                
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.get_by_username(username)
        # 對照輸入的密碼與資料庫中的雜湊結果是否吻合
        if user and check_password_hash(user.password_hash, password):
            # 登入成功寫入 Session
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'歡迎回來，{user.username}！準備好接受神明的指引了嗎？', 'success')
            
            # 若為首頁或特定預設跳轉，這邊直接回首頁
            return redirect(url_for('main.index'))
        else:
            flash('登入失敗，帳號或密碼錯誤。', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear() # 清空 session
    flash('您已成功順利登出。', 'info')
    return redirect(url_for('main.index'))
