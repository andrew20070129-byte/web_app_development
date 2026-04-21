from flask import render_template, request, redirect, url_for, flash, session
from . import auth_bp

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    使用者註冊路由
    GET: 渲染 templates/auth/register.html，顯示註冊表單
    POST: 接收表單傳入的帳號、信箱、密碼等，進行驗證與寫入資料庫
          成功後重導向至 /auth/login
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    使用者登入路由
    GET: 渲染 templates/auth/login.html，顯示登入表單
    POST: 接收帳號密碼進行驗證，成功則寫入 session 狀態，重導向至首頁大廳
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    使用者登出路由
    清空 session 的登入狀態，重導向至首頁
    """
    pass
